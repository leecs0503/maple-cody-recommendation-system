import logging
from http import HTTPStatus

from aiohttp import web

from ..server.config import Config
import requests
from bs4 import BeautifulSoup
import json


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
            web.post('/character_code_web_handler', self.character_code_web_handler),
            web.post('/infer_code_web_handler', self.infer_code_web_handler),
        ]

    async def index_handler(self, request: web.Request):
        """ """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def healthcheck_handler(self, request: web.Request):
        """ """
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    async def character_code_web_handler(self, request: web.Request) -> web.Response:

        post = await request.text()
        post = json.loads(post)
        self.logger.info(f"web server character request information: {post}")

        res = post['name']

        url = f'https://maple.gg/u/{res}'
        soup = get_html_text(url)

        img_tag = soup.find_all(class_="character-image")[1]["src"]
        self.logger.info(f"crawling character url : {img_tag}")

        encrypted_code = img_tag.replace('https://avatar.maplestory.nexon.com/Character/', '').replace('.png', '')
        response = requests.post("http://localhost:8080/packed_character_look", json={"packed_character_look": encrypted_code})
        self.logger.info(f"web server character code response: {response.text}")

        return web.Response(body=response.text, status=HTTPStatus.OK)

    async def infer_code_web_handler(self, request: web.Request) -> web.Response:

        post = await request.text()
        post = json.loads(post)
        post = post["character_code_result"]
        self.logger.info(f"inference request text : {post}")

        # response = requests.post("http://localhost:8080/inference", post)  -> infer 서버에 사용자의 코드 요청
        # 추천된 코드를 json으로 저장하여 response로 받는다고 가정

        response = '{"face": "54002", "cap": "1005041", "longcoat": "1053240", "weapon": "1703048", "cape": "1103332", "coat": "0", "glove": "1082703", "hair": "61481+3*50", "pants": "0", "shield": "1092067", "shoes": "1073534", "faceAccessory": "1012050", "eyeAccessory": "1022079", "earrings": "1032022", "skin": "12024"}'
        response = json.loads(response)
        self.logger.info(f"inference character code : {response}")

        obj = {}
        for k, v in response.items():
            if k == 'skin':
                k = 'head'
            if k == 'shield':
                continue
            if v == '0':
                continue
            if k == 'name':
                continue
            obj[k] = v

        obj['bs'] = 'true'

        encoding_images = {}

        for k, v in obj.items():
            if k == 'bs':
                continue
            url = f'https://0.0.0.0:7209/{k}/?code={v}&bs=true'
            res = requests.get(url, verify=False)
            encoding_images[k] = res.text
            self.logger.info(f"add encoding image element : {k} : {res.text}")

        res = requests.get('https://0.0.0.0:7209/avatar', params=obj, verify=False)

        self.logger.info(f"bs64 encoded inference image string : {res.text}")
        encoding_images['avatar'] = res.text

        return web.json_response(encoding_images)
