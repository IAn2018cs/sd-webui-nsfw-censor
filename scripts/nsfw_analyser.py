# coding=utf-8
import os
import tempfile
from typing import Tuple

from PIL import Image

from nsfw.core import run


def image_analyser(
	replacement_img: Image.Image,
	target_img: Image.Image,
	min_threshold: float
) -> Tuple[Image.Image, float]:
	if isinstance(replacement_img, str):  # source_img is a base64 string
		import base64, io
		if 'base64,' in replacement_img:  # check if the base64 string has a data URL scheme
			base64_data = replacement_img.split('base64,')[-1]
			img_bytes = base64.b64decode(base64_data)
		else:
			# if no data URL scheme, just decode
			img_bytes = base64.b64decode(replacement_img)
		replacement_img = Image.open(io.BytesIO(img_bytes))

	target_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
	target_img.save(target_path)

	result, probability = run(target_path, min_threshold)
	if result is None:
		result_image = target_img
	elif result:
		result_image = replacement_img
	else:
		result_image = target_img

	# clear temp files
	try:
		os.remove(target_path)
	except Exception as e:
		print(f"delete tmp file error: {e}")

	return result_image, probability
