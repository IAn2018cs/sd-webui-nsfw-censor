import os

import filetype


def is_file(file_path: str) -> bool:
	return bool(file_path and os.path.isfile(file_path))


def is_image(image_path: str) -> bool:
	return is_file(image_path) and filetype.helpers.is_image(image_path)


def resolve_relative_path(path: str) -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), path))
