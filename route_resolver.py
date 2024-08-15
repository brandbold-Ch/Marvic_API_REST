import os

context_route = os.path.dirname(__file__)


def static_files(file: str) -> str:
    return os.path.join(context_route, "static", "images", file)

