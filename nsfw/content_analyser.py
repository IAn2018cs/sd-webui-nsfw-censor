import threading
from functools import lru_cache
from time import sleep
from typing import Any, Dict

import cv2
import numpy
import onnxruntime

import nsfw.globals
from nsfw import process_manager
from nsfw.download import conditional_download
from nsfw.execution import apply_execution_provider_options
from nsfw.filesystem import resolve_relative_path
from nsfw.typings import VisionFrame, ModelValue
from nsfw.vision import read_image

CONTENT_ANALYSER = None
THREAD_LOCK: threading.Lock = threading.Lock()
MODELS: Dict[str, ModelValue] = \
	{
		'open_nsfw':
			{
				'url': 'https://github.com/facefusion/facefusion-assets/releases/download/models/open_nsfw.onnx',
				'path': resolve_relative_path('../.assets/models/open_nsfw.onnx')
			}
	}


def get_content_analyser() -> Any:
	global CONTENT_ANALYSER

	with THREAD_LOCK:
		while process_manager.is_checking():
			sleep(0.5)
		if CONTENT_ANALYSER is None:
			model_path = MODELS.get('open_nsfw').get('path')
			CONTENT_ANALYSER = onnxruntime.InferenceSession(model_path, providers=apply_execution_provider_options(
				nsfw.globals.execution_providers))
	return CONTENT_ANALYSER


def clear_content_analyser() -> None:
	global CONTENT_ANALYSER

	CONTENT_ANALYSER = None


def pre_check() -> bool:
	if not nsfw.globals.skip_download:
		download_directory_path = resolve_relative_path('../.assets/models')
		model_url = MODELS.get('open_nsfw').get('url')
		process_manager.check()
		conditional_download(download_directory_path, [model_url])
		process_manager.end()
	return True


def analyse_frame(vision_frame: VisionFrame) -> bool:
	content_analyser = get_content_analyser()
	vision_frame = prepare_frame(vision_frame)
	probability = content_analyser.run(None,
									   {
										   content_analyser.get_inputs()[0].name: vision_frame
									   })[0][0][1]
	return probability > nsfw.globals.probability_limit


def prepare_frame(vision_frame: VisionFrame) -> VisionFrame:
	vision_frame = cv2.resize(vision_frame, (224, 224)).astype(numpy.float32)
	vision_frame -= numpy.array([104, 117, 123]).astype(numpy.float32)
	vision_frame = numpy.expand_dims(vision_frame, axis=0)
	return vision_frame


@lru_cache(maxsize=None)
def analyse_image(image_path: str) -> bool:
	frame = read_image(image_path)
	return analyse_frame(frame)
