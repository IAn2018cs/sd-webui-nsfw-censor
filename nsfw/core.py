import os

os.environ['OMP_NUM_THREADS'] = '1'

import warnings
import onnxruntime
from time import time
from typing import Optional, Tuple

from nsfw import content_analyser
from nsfw.content_analyser import image_nsfw_probability
from nsfw.filesystem import is_image
from nsfw import logger
from nsfw.execution import decode_execution_providers
import nsfw.globals

onnxruntime.set_default_logger_severity(3)
warnings.filterwarnings('ignore', category=UserWarning, module='gradio')


def run(path: str, limit: float = 0.8) -> Tuple[Optional[bool], float]:
	nsfw.globals.skip_download = False
	nsfw.globals.log_level = 'info'
	nsfw.globals.probability_limit = limit
	# execution
	provider = "cuda"
	providers = decode_execution_providers([provider])
	if len(providers) == 0:
		providers = decode_execution_providers(['cpu'])
	nsfw.globals.execution_providers = providers
	logger.info(f"device use {nsfw.globals.execution_providers}", __name__.upper())

	if not content_analyser.pre_check():
		return None, 0
	start_time = time()
	if is_image(path):
		return process_image(path, start_time, limit)
	return None, 0


def process_image(path: str, start_time: float, limit: float) -> Tuple[bool, float]:
	nsfw_probability = image_nsfw_probability(path)
	is_nsfw = nsfw_probability > limit
	seconds = '{:.2f}'.format((time() - start_time) % 60)
	logger.info(f"analyse_image cost time: {seconds}s", __name__.upper())
	if is_nsfw:
		logger.info(f"skip process, source image is nsfw", __name__.upper())
		return True, nsfw_probability
	return False, nsfw_probability
