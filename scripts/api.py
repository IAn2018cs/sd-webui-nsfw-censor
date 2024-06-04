import os
import tempfile

import gradio as gr
from fastapi import FastAPI, Body
from modules.api import api
from modules.api.models import *

from nsfw.core import run


def rembg_api(_: gr.Blocks, app: FastAPI):
	@app.post("/nsfw-censor")
	async def nsfw_censor(
		input_image: str = Body("", title='input image'),
	):
		input_image = api.decode_base64_to_image(input_image)
		target_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
		input_image.save(target_path)

		result = run(target_path)
		if result is None:
			is_nsfw = False
		elif result:
			is_nsfw = True
		else:
			is_nsfw = False

		# clear temp files
		try:
			os.remove(target_path)
		except Exception as e:
			print(f"delete tmp file error: {e}")

		return {"is_nsfw": is_nsfw}


try:
	import modules.script_callbacks as script_callbacks

	script_callbacks.on_app_started(rembg_api)
except:
	pass