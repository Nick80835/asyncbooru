from logging import getLogger
from typing import List

from aiohttp import ClientSession

logger = getLogger(__name__)
api_url = "https://gelbooru.com/index.php"
sauce_base = "https://gelbooru.com/index.php?page=post&s=view&id="

ratings = {
    ("safe", "s"): "Rating:safe",
    ("questionable", "q"): "Rating:questionable",
    ("explicit", "e", "x"): "Rating:explicit"
}


class GelbooruPost:
    def __init__(self, json: dict):
        self.json = json
        self.id: int = json.get("id")
        self.file_url: str = json.get("file_url")
        self.rating: str = json.get("rating")
        self.height: int = json.get("height")
        self.width: int = json.get("width")
        self.hash: str = json.get("hash")
        self.tags: str = json.get("tags")
        self.score: int = json.get("score")
        self.source: str = json.get("source")
        self.owner: str = json.get("owner")
        self.created_at: str = json.get("created_at")
        self.parent_id: int = json.get("parent_id")
        self.sauce: str = sauce_base + str(self.id)


class Gelbooru:
    def __init__(self, client=ClientSession()):
        self.client = client

    async def get_random_post(self, tags: str = "", rating: str = "") -> GelbooruPost:
        return GelbooruPost((await self.json_request(f"sort:random {tags}", 1, rating))[0])

    async def get_random_posts(self, tags: str = "", limit: int = 30, rating: str = "") -> List[GelbooruPost]:
        return [GelbooruPost(json) for json in await self.json_request(f"sort:random {tags}", limit, rating)]

    async def get_latest_post(self, tags: str = "", rating: str = "") -> GelbooruPost:
        return GelbooruPost((await self.json_request(f"{tags}", 1, rating))[0])

    async def get_latest_posts(self, tags: str = "", limit: int = 30, rating: str = "") -> List[GelbooruPost]:
        return [GelbooruPost(json) for json in await self.json_request(tags, limit, rating)]

    async def json_request(self, tags: str = "", limit: int = 30, rating: str = "") -> dict:
        params = {"page": "dapi",
                  "s": "post",
                  "q": "index",
                  "json": 1,
                  "limit": limit,
                  "tags": f"{self._get_rating(rating)} {tags}".strip()}

        logger.debug("Handling request for tags: %s", params.get('tags'))

        async with self.client.get(api_url, params=params) as response:
            if response.status == 200:
                return await response.json()

            raise Exception

    @staticmethod
    def _get_rating(rating: str) -> str:
        rating_res = [v for k, v in ratings.items() if rating.lower() in k]
        return rating_res[0] if rating_res else ""
