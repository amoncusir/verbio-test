from typing import TYPE_CHECKING, Optional

from dependency_injector import providers

from src.module.common.command import Command


class ApplicationScoped(providers.Singleton):
    pass


class RequestScoped(providers.Factory):
    pass


class RouteProvider(ApplicationScoped):
    pass


class SubscriberProvider(ApplicationScoped):
    pass


class QueryProvider(providers.Factory):
    pass


class CommandProvider(providers.Provider):
    __slots__ = (
        "_factory",
        "_reference",
    )

    def __init__(self, command: type[Command], *args, **kwargs):
        if not issubclass(command, Command):
            raise TypeError("command must be a subclass of Command")

        self._factory = providers.Factory(command, *args, **kwargs)
        self._reference = None
        super().__init__()

    def with_reference(self, reference: str):
        self._reference = reference
        return self

    @property
    def cls(self) -> type[Command]:
        return self._factory.cls

    @property
    def is_referencable(self) -> bool:
        return self._reference is not None

    @property
    def reference(self) -> Optional[str]:
        return self._reference

    def __deepcopy__(self, memo):
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(
            self._factory.provides,
            *providers.deepcopy(self._factory.args, memo),
            **providers.deepcopy(self._factory.kwargs, memo),
        ).with_reference(self._reference)

        self._copy_overridings(copied, memo)

        return copied

    @property
    def related(self):
        """Return related providers generator."""
        yield from [self._factory]
        yield from super().related

    def _provide(self, args, kwargs):
        return self._factory(*args, **kwargs)

    if TYPE_CHECKING:

        def __call__(self) -> Command: ...


class RepositoryProvider(RequestScoped):
    pass
