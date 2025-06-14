import pytest
from fastapi.testclient import TestClient

from src.app.application import Application
from src.app.container import MainContainer


@pytest.fixture(scope="function")
def client(application) -> TestClient:
    return TestClient(application.fastapi())


@pytest.fixture(scope="function")
def application():

    # Override in runtime the configuration
    config = {}

    app = Application.init_with_container(MainContainer, config, "./config/development.yaml")

    yield app

    print(f"Used Application::Config - {app.container.config()}")

    # Clear the Singleton instance for the next execution
    Application.remove_instance()
