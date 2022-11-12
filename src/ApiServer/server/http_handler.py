import logging
from http import HTTPStatus

from aiohttp import web

from ..server.config import Config
import requests
from bs4 import BeautifulSoup


def get_html_text(url: str):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


class HTTPHandler:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ):
        self.logger = logger

    def get_routes(self):
        return [
            web.get("/", self.index_handler),
            web.get("/healthcheck", self.healthcheck_handler),
            web.post('/web_handler', self.web_handler)
        ]

    async def index_handler(self, request: web.Request):
        """ """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def healthcheck_handler(self, request: web.Request):
        """ """
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    async def web_handler(self, request: web.Request):

        post = await request.text()
        res = dict()
        post = post.replace('{' , '').replace('}' , '').replace('"' , '')
        post = post.split(':')
        res = post[1]

        url = f'https://maple.gg/u/{res}'
        soup = get_html_text(url)
        img_tag = soup.find_all(class_="character-image")[1:-1]
        tag_list = [tag["src"] for tag in img_tag]
        tag = tag_list[0]

        encrypted_code = tag.replace('https://avatar.maplestory.nexon.com/Character/', '').replace('.png', '')
        response = requests.post("http://localhost:8080/packed_character_look", json={"packed_character_look": encrypted_code})
        print(response.text)

        return web.Response(body=response.text, status=HTTPStatus.OK)
