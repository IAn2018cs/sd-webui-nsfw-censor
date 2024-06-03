import os

os.environ['OMP_NUM_THREADS'] = '1'

import warnings
import onnxruntime
from time import time
from typing import Optional

from nsfw import content_analyser
from nsfw.content_analyser import analyse_image
from nsfw.filesystem import is_image
from nsfw import logger
from nsfw.execution import decode_execution_providers
import nsfw.globals

onnxruntime.set_default_logger_severity(3)
warnings.filterwarnings('ignore', category=UserWarning, module='gradio')


def run(path: str) -> Optional[bool]:
	nsfw.globals.skip_download = False
	nsfw.globals.log_level = 'info'
	# execution
	provider = "cuda"
	providers = decode_execution_providers([provider])
	if len(providers) == 0:
		providers = decode_execution_providers(['cpu'])
	nsfw.globals.execution_providers = providers
	logger.info(f"device use {nsfw.globals.execution_providers}", __name__.upper())

	if not content_analyser.pre_check():
		return None
	start_time = time()
	if is_image(path):
		return process_image(path, start_time)
	return None


def process_image(path: str, start_time: float) -> Optional[bool]:
	is_nsfw = analyse_image(path)
	seconds = '{:.2f}'.format((time() - start_time) % 60)
	logger.info(f"analyse_image cost time: {seconds}s", __name__.upper())
	if is_nsfw:
		logger.info(f"skip process, source image is nsfw", __name__.upper())
		return True
	return False
