import logging
import ssl
from typing import Any, Callable, Awaitable

from faststream import FastStream
from faststream.rabbit import (
    ExchangeType,
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
    RabbitRoute,
    RabbitRouter,
    QueueType,
    Channel,
)
from faststream.security import BaseSecurity

from src.app.rabbitmq.subscriber import FastRabbitHandler
from src.config.app import AppConfig
from src.app.rabbitmq.settings import RabbitMQSettings, RabbitMQTaskSettings, RabbitMQEventSettings

FAST_STREAM_PROFILE = "disable-fast-stream"

logger = logging.getLogger(__name__)


def build_fast_stream(
    settings: RabbitMQSettings, broker: RabbitBroker, subscribers: list[FastRabbitHandler]
) -> FastStream:

    app = FastStream(broker)

    @app.after_startup
    async def on_startup():
        await declare_and_bind_task_dlq(settings.task, broker)
        await declare_and_bind_event_dlq(settings.event, broker, subscribers)

    return app


async def fast_stream_initializer(app: FastStream, app_config: AppConfig):
    if not app_config.contains_profile(FAST_STREAM_PROFILE):
        await app.start()
        yield
        await app.stop()
    else:
        logger.warning("Fast stream is disabled")
        yield


def build_tls_security_settings() -> BaseSecurity:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

    return BaseSecurity(ssl_context, use_ssl=True)


def build_rabbitmq_broker(
    app_config: AppConfig, rabbitmq_settings: RabbitMQSettings, event_router: RabbitRouter, task_router: RabbitRouter
) -> RabbitBroker:
    security = None

    if rabbitmq_settings.security:
        security = build_tls_security_settings()

    channel = Channel(
        prefetch_count=rabbitmq_settings.max_consumers,
        publisher_confirms=True,
        on_return_raises=True,
    )

    broker = RabbitBroker(
        app_id=app_config.name,
        fail_fast=True,
        on_return_raises=True,
        url=rabbitmq_settings.url,
        security=security,
        default_channel=channel,
        graceful_timeout=rabbitmq_settings.graceful_timeout,
        timeout=rabbitmq_settings.connection_timeout,
        log_level=app_config.int_log_level,
    )

    broker.include_router(event_router, prefix="event.", include_in_schema=True)
    broker.include_router(task_router, include_in_schema=False)

    return broker


#  Event ###############################################################################################################


def build_event_exchange(settings: RabbitMQEventSettings) -> RabbitExchange:
    return RabbitExchange(settings.exchange_name, ExchangeType.TOPIC, auto_delete=settings.auto_delete)


def build_event_rabbit_router(
    settings: RabbitMQEventSettings, exchange: RabbitExchange, subscribers: list[FastRabbitHandler]
) -> RabbitRouter:
    def _build_event_route_handler(handler: FastRabbitHandler) -> RabbitRoute:
        queue = RabbitQueue(
            handler.name,
            QueueType.QUORUM,
            routing_key=handler.routing_key,
            arguments={
                "x-dead-letter-exchange": settings.dead_letter_exchange_name,
            },
        )

        route = RabbitRoute(handler.callable, queue, exchange=exchange, **handler.args)

        logger.debug("Created event queue: %s for %s", handler.name, handler)

        return route

    return RabbitRouter(handlers=(_build_event_route_handler(sub) for sub in subscribers))


def rabbit_publisher(exchange: str | RabbitExchange, broker: RabbitBroker):
    async def wrap(routing_key: str, msg: Any, **kwargs):
        logger.info(
            "Publishing message to exchange: %s with routing key: event.%s and body: %s",
            exchange.name,
            routing_key,
            msg,
        )
        result = await broker.publish(
            msg, mandatory=False, routing_key=f"event.{routing_key}", exchange=exchange, **kwargs
        )
        logger.debug(
            "Published message to exchange: %s with routing key: event.%s and result: %s",
            exchange.name,
            routing_key,
            result,
        )
        return result

    return wrap


async def declare_and_bind_event_dlq(
    settings: RabbitMQEventSettings, broker: RabbitBroker, subscribers: list[FastRabbitHandler]
):

    exchange_def = RabbitExchange(
        settings.dead_letter_exchange_name, ExchangeType.TOPIC, auto_delete=False, durable=True, robust=True
    )
    exchange = await broker.declare_exchange(exchange_def)

    for subscriber in subscribers:
        queue_def = RabbitQueue(
            subscriber.dlq_name,
            auto_delete=False,
            durable=True,
        )

        queue = await broker.declare_queue(queue_def)
        await queue.bind(exchange=exchange, routing_key=subscriber.routing_key, robust=True)
        logger.debug("Created event queue.dlq: %s for %s", subscriber.dlq_name, subscriber)


#  Task ################################################################################################################


def build_task_exchange(settings: RabbitMQTaskSettings) -> RabbitExchange:
    return RabbitExchange(settings.exchange_name, ExchangeType.DIRECT, auto_delete=False, durable=True)


def build_task_rabbit_queue(settings: RabbitMQTaskSettings) -> RabbitQueue:
    queue = RabbitQueue(
        settings.route_key,
        QueueType.QUORUM,
        routing_key=settings.route_key,
        auto_delete=False,
        durable=True,
        arguments={
            "x-dead-letter-exchange": settings.dead_letter_exchange_name,
            "x-dead-letter-routing-key": settings.dead_letter_route_key,
        },
    )

    logger.debug("Created task queue: %s -> %s by %s", queue.name, queue.routing_key, settings)

    return queue


def build_task_rabbit_router(
    settings: RabbitMQTaskSettings, queue: RabbitQueue, exchange: RabbitExchange, handler: Callable[..., Awaitable]
) -> RabbitRouter:
    return RabbitRouter(
        handlers=(RabbitRoute(handler, queue=queue, exchange=exchange, retry=settings.default_retries),),
    )


async def declare_and_bind_task_dlq(settings: RabbitMQTaskSettings, broker: RabbitBroker):
    exchange_def = RabbitExchange(
        settings.dead_letter_exchange_name, ExchangeType.DIRECT, auto_delete=False, durable=True, robust=True
    )

    queue_def = RabbitQueue(
        settings.dead_letter_route_key,
        auto_delete=False,
        durable=True,
    )

    exchange = await broker.declare_exchange(exchange_def)
    queue = await broker.declare_queue(queue_def)

    await queue.bind(exchange=exchange, routing_key=settings.dead_letter_route_key, robust=True)
