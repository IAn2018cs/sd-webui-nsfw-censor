from functools import lru_cache
from typing import Optional, List

import cv2

from nsfw.filesystem import is_image
from nsfw.typings import VisionFrame


@lru_cache(maxsize=128)
def read_static_image(image_path: str) -> Optional[VisionFrame]:
	return read_image(image_path)


def read_static_images(image_paths: List[str]) -> Optional[List[VisionFrame]]:
	frames = []
	if image_paths:
		for image_path in image_paths:
			frames.append(read_static_image(image_path))
	return frames


def read_image(image_path: str) -> Optional[VisionFrame]:
	if is_image(image_path):
		return cv2.imread(image_path)
	return None
