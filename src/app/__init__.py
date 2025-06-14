from .application import Application


def get_app() -> Application:
    return Application()


__all__ = [
    "get_app",
    "Application",
]
