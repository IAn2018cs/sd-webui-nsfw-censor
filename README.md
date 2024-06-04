# NSFW Censor extension for StableDiffusion Webui

This repo makes it an extension of [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui/) or [Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) Webui.

![Preview](.github/preview.png)

## Installation

-   Clone this repo into `stable-diffusion-webui/extensions` folder.
-   Start the Webui.

## SD webui alwayson_scripts api

```python
alwayson_scripts = {
  "nsfw-censor": {
    "args": [
      # nsfw picture replacement picture
      get_base64_image('./replacement.png'),
      # Enable
      True
    ]
  }
}
```

## only api

```python
url = 'http://localhost:7860/nsfw-censor'
data = {
    "input_image": get_base64_image('./test_img/t1.png'),
    "threshold": 0.8
}
response = requests.request("POST", url,
                            headers={
                                'Content-Type': 'application/json'
                            },
                            data=json.dumps(data))
result = response.json()
print(response.text)
# print
# {"is_nsfw":false}
is_nsfw = result['is_nsfw']
print(f"image is nsfw: {is_nsfw}")
# print
# image is nsfw: False
```

