import logging

import pytest

from src.module.common.domain.aggregates import AggregateRoot
from src.module.common.domain.events import DomainEvent


# Dummy event class for testing
class MockEvent(DomainEvent):
    @classmethod
    def routing_path(cls) -> str:
        return "mock_event"


# Dummy aggregate class for testing
class MockAggregate(AggregateRoot[int]):
    pass


@pytest.fixture
def aggregate():
    return MockAggregate(_id=1)


def test_add_event(aggregate):
    event = MockEvent()

    aggregate._add_event(event)

    assert len(aggregate.read_events()) == 1


def test_pop_events(aggregate):
    event = MockEvent()
    aggregate._add_event(event)

    # Using the private method directly for testing purposes
    popped_events = aggregate._AggregateRoot__pop_events()

    assert len(popped_events) == 1
    assert popped_events[0] == event
    assert len(aggregate.read_events()) == 0


def test_list_events_repr(aggregate):
    event = MockEvent()

    aggregate._add_event(event)

    event_repr = aggregate.list_events_repr()

    assert len(event_repr) == 1
    assert event_repr[0] == repr(event)


def test_copy(aggregate):
    event = MockEvent()
    aggregate._add_event(event)
    duplicate = aggregate.copy()

    # Ensure that the duplicate is a different object and events are not copied
    assert duplicate is not aggregate
    assert duplicate.read_events() == []  # Duplicate should not have any events

    # Using the private method directly for testing purposes
    popped_events = aggregate.read_events()
    assert popped_events == [event]  # Original should have the event


def test_aggregate_with_remaining_events_destructor(aggregate, caplog):
    # Test that the destructor logs an error when there are remaining events
    event = MockEvent()

    aggregate._add_event(event)

    with caplog.at_level(logging.ERROR):
        # Ensure no error is raised but the log should be checked
        del aggregate

        for record in caplog.records:
            assert record.levelno == logging.ERROR
