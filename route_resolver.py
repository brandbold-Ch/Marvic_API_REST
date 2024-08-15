import os

context_route = os.path.dirname(__file__)


def get_image_path(file: str) -> str:
    return os.path.join(context_route, "static", "images", file)
