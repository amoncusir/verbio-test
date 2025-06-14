import threading
from typing import Any

from dependency_injector.containers import DeclarativeContainer


class Singleton(type):
    _instances = {}
    __lock = threading.Lock()  # Not the best, but enough for the current use

    def __call__(cls, *args, **kwargs):

        # Check if bypass flag is passed, and if so, create a new instance
        bypass_singleton = kwargs.pop("bypass_singleton", False)

        if bypass_singleton:
            return super(Singleton, cls).__call__(*args, **kwargs)

        # Standard singleton behavior
        if cls not in cls._instances:
            with cls.__lock:
                # dic assignation is not an atomic operation
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

    @classmethod
    def remove_instance(mcs, target_cls):

        if target_cls in mcs._instances:
            del mcs._instances[target_cls]


def find_providers(container: DeclarativeContainer, provider_type: Any):
    return [p() for p in container.traverse(types=[provider_type])]
