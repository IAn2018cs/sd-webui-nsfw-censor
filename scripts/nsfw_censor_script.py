# coding=utf-8

import gradio as gr
from PIL import Image
from modules import scripts, images, scripts_postprocessing
from modules.processing import (
	StableDiffusionProcessing,
)

from scripts.nsfw_analyser import image_analyser
from scripts.nsfw_utils import get_timestamp

sc_name = "NSFW-CENSOR"
version = "1.0"

print(
	f"[-] NSFW-CENSOR initialized. version: {version}"
)


class NsfwCensorScript(scripts.Script):
	def title(self):
		return sc_name

	def show(self, is_img2img):
		return scripts.AlwaysVisible

	def ui(self, is_img2img):
		with gr.Accordion(sc_name, open=False):
			with gr.Column():
				with gr.Row():
					gr.Markdown(value=f"v{version}")
				with gr.Row():
					img = gr.Image(type="pil", label="nsfw picture replacement picture")
				with gr.Row():
					enable = gr.Checkbox(False, placeholder="enable", label="Enable")
		return [
			img,
			enable
		]

	def process(
		self,
		p: StableDiffusionProcessing,
		img,
		enable
	):
		self.replacement_img = img
		self.enable = enable
		if self.enable:
			if self.replacement_img is None:
				print(f"Please provide a replacement img")

	def postprocess_batch(self, *args, **kwargs):
		if self.enable:
			return images

	def postprocess_image(self, p, script_pp: scripts.PostprocessImageArgs, *args):
		if self.enable:
			if self.replacement_img is not None:
				st = get_timestamp()
				print(f"{sc_name} enabled, start process")
				image: Image.Image = script_pp.image

				result: Image.Image = image_analyser(
					self.replacement_img,
					image
				)
				pp = scripts_postprocessing.PostprocessedImage(result)
				pp.info = {}
				p.extra_generation_params.update(pp.info)
				script_pp.image = pp.image
				et = get_timestamp()
				cost_time = (et - st) / 1000
				print(f"{sc_name} process done, time taken: {cost_time} sec.")
