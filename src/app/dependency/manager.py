from dataclasses import dataclass
from typing import Iterable, TYPE_CHECKING

from dependency_injector.containers import Container

from src.module.common.query import Query
from src.module.providers import CommandProvider, QueryProvider

if TYPE_CHECKING:
    from src.module.common.command import Command


@dataclass(frozen=True)
class DependencyManager:
    container: Container

    @property
    def command_references(self) -> Iterable[CommandProvider]:
        return self.container.traverse(types=[CommandProvider])

    @property
    def query_references(self) -> Iterable[QueryProvider]:
        return self.container.traverse(types=[QueryProvider])

    def find_command_by_ref(self, reference: str) -> CommandProvider:
        for provider in self.command_references:
            if provider.reference == reference and provider.is_referencable:
                return provider

        raise KeyError(f"Command with reference {reference} not found.")

    def find_command_by_type(self, reference: type) -> CommandProvider:
        for provider in self.command_references:
            if provider.cls == reference:
                return provider

        raise KeyError(f"Command {reference} not found.")

    def find_command_reference(self, command: type['Command']) -> str:
        for provider in self.command_references:
            if provider.cls == command and provider.is_referencable:
                return provider.reference

        raise KeyError(f"Command {command} not found.")

    def find_query_by_type(self, reference: type[Query]) -> QueryProvider:
        for provider in self.query_references:
            if issubclass(provider.cls, reference):
                return provider

        raise KeyError(f"Query {reference} not found.")
