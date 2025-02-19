import os
from typing import Dict, Union, TypedDict

import fasttext
import aiohttp

models = {"low_mem": None, "high_mem": None}
FTLANG_CACHE = os.getenv("FTLANG_CACHE", "/tmp/fasttext-langdetect")


class DetectionResponse(TypedDict):
    lang: str
    score: float


async def download_model(name: str, path = None) -> str:
    target_path = os.path.join(FTLANG_CACHE, name) if not path else path
    if not os.path.exists(target_path):
        url = f"https://dl.fbaipublicfiles.com/fasttext/supervised-models/{name}"  # noqa
        os.makedirs(FTLANG_CACHE, exist_ok=True)
        with open(target_path, "wb") as fp:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    fp.write(await response.read())
    return target_path


async def get_or_load_model(low_memory=False, path = None):
    if low_memory:
        model = models.get("low_mem", None)
        if not model:
            model_path = await download_model("lid.176.ftz", path)
            try:
                # silences warnings as the package does not properly use the python 'warnings' package
                # see https://github.com/facebookresearch/fastText/issues/1056
                fasttext.FastText.eprint = lambda *args,**kwargs: None
            except:
                pass
            model = fasttext.load_model(model_path)
            models["low_mem"] = model
        return model
    else:
        model = models.get("high_mem", None)
        if not model:
            model_path = await download_model("lid.176.bin", path)
            model = fasttext.load_model(model_path)
            models["high_mem"] = model
        return model


async def detect(text: str, low_memory: bool = False, path = None) -> DetectionResponse:
    model = await get_or_load_model(low_memory, path)
    labels, scores = model.predict(text)
    label = labels[0].replace("__label__", '')
    score = min(float(scores[0]), 1.0)
    return {
        "lang": label,
        "score": score,
    }
