import requests
import json
from typing import Any

from .types import NSFWOption

class CatgirlDownloaderAPI:
    def __init__(self) -> None:
        self.endpoint = "https://nekos.moe/api/v1/random/image"
        self.info = None

    def get_random_image_info(self, nsfw_mode: NSFWOption = NSFWOption.BLOCK_NSFW) -> dict | None:
        try:
            url = self.endpoint
            if nsfw_mode == "Only NSFW":
                url += "?nsfw=true"
            elif nsfw_mode == "Block NSFW":
                url += "?nsfw=false"

            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return None
        except Exception as e:
            print(e)
            return None

        data = json.loads(r.text)
        self.info = data
        return data

    def get_random_image_id(self, nsfw_mode: NSFWOption = NSFWOption.BLOCK_NSFW) -> str | None:
        data = self.get_random_image_info(nsfw_mode)
        if not data or "images" not in data or not data["images"]:
            return None
        return data["images"][0].get("id")

    def get_image_url(self, nsfw_mode: NSFWOption = NSFWOption.BLOCK_NSFW) -> str | None:
        data = self.get_random_image_info(nsfw_mode)
        if not data or "images" not in data or not data["images"]:
            return None

        image = data["images"][0]

        original_hash = image.get("originalHash")
        if original_hash:
            return "https://nekos.moe/image/original/" + original_hash

        image_id = image.get("id")
        if image_id:
            return "https://nekos.moe/image/" + image_id

        return None

    def get_image(self, url: str) -> bytes | Any:
        r = requests.get(url, timeout=20)
        return r.content
