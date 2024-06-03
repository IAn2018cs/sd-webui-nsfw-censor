# coding=utf-8
import os
import tempfile

from PIL import Image

from nsfw.core import run


def image_analyser(
	target_img: Image.Image
) -> Image.Image:
	target_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
	target_img.save(target_path)

	result = run(target_path)
	if result is None:
		result_image = target_img
	elif result:
		result_image = None
	else:
		result_image = target_img

	# clear temp files
	try:
		os.remove(target_path)
	except Exception as e:
		print(f"delete tmp file error: {e}")

	return result_image
