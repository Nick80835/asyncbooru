from typing import List

from aiohttp import ClientSession


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


class Gelbooru:
    api_url = "https://gelbooru.com/index.php"

    def __init__(self, client=ClientSession()):
        self.client = client

    async def get_random_post(self, tags: str = "") -> GelbooruPost:
        return GelbooruPost((await self.json_request(f"sort:random {tags}", 1))[0])

    async def get_random_post_list(self, tags: str = "", limit: int = 30) -> List[GelbooruPost]:
        return [GelbooruPost(json) for json in await self.json_request(f"sort:random {tags}", limit)]

    async def json_request(self, tags: str = "", limit: int = 30) -> dict:
        params = {"page": "dapi",
                  "s": "post",
                  "q": "index",
                  "json": 1,
                  "limit": limit,
                  "tags": tags.strip()}

        async with self.client.get(self.api_url, params=params) as response:
            if response.status == 200:
                return await response.json()

            raise Exception
