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

def get_avatar_item_encoding_string(response_infer_code: dict) -> dict:
    wz_server_url = 'https://0.0.0.0:7209/avatar'
    obj = {}
    encoding_images = {}

    for k, v in response_infer_code.items():
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

    for k, v in obj.items():
        if k == 'bs':
            continue
        item_image_url = f'https://0.0.0.0:7209/{k}/?code={v}&bs=true'
        res = requests.get(item_image_url, verify=False)
        encoding_images[k] = res.text
    res = requests.get(wz_server_url, params=obj, verify=False)
    encoding_images['avatar'] = res.text

    return encoding_images



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
            web.get("/get_wz_code", self.get_wz_code),
            web.post('/character_code_web_handler', self.character_code_web_handler),
            web.post('/infer_code_web_handler', self.infer_code_web_handler),
        ]

    async def index_handler(self, request: web.Request):
        """ """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def healthcheck_handler(self, request: web.Request):
        """ """
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    async def get_wz_code(self, request: web.Request) -> web.json_response:
        url = 'https://0.0.0.0:7209/code'
        res = requests.get(url, verify=False)
        json_wz_code = json.loads(res.text)

        return web.json_response(json_wz_code)

    async def character_code_web_handler(self, request: web.Request) -> web.Response:
        avatar_server_url ="http://localhost:8080/packed_character_look"
        maple_gg_url = f'https://maple.gg/u/{res}'

        post = await request.text()
        post = json.loads(post)
        self.logger.info(f"web server character request information: {post}")
        res = post['name']

        soup = get_html_text(maple_gg_url)

        img_tag = soup.find_all(class_="character-image")[1]["src"]
        self.logger.info(f"crawling character url : {img_tag}")

        encrypted_code = img_tag.replace('https://avatar.maplestory.nexon.com/Character/', '').replace('.png', '')
        response = requests.post(avatar_server_url, json={"packed_character_look": encrypted_code})
        self.logger.info(f"web server character code response: {response.text}")

        return web.Response(body=response.text, status=HTTPStatus.OK)

    async def infer_code_web_handler(self, request: web.Request) -> web.json_response:
        result_inference = {}
        encoding_images = {}

        post = await request.text()
        post = json.loads(post)
        post = post["character_code_result"]
        self.logger.info(f"inference request text : {post}")

        # response = requests.post("http://localhost:8080/inference", post)  -> infer 서버에 사용자의 코드 요청
        # 추천된 코드를 json으로 저장하여 response로 받는다고 가정

        response_infer_code = '{"face": "54002", "cap": "1005041", "longcoat": "1053240", "weapon": "1703048", "cape": "1103332", "coat": "0", "glove": "1082703", "hair": "61481+3*50", "pants": "0", "shield": "1092067", "shoes": "1073534", "faceAccessory": "1012050", "eyeAccessory": "1022079", "earrings": "1032022", "skin": "12024"}'
        response_infer_code = json.loads(response_infer_code)
        self.logger.info(f"inference character code : {response_infer_code}")

        encoding_images = get_avatar_item_encoding_string(response_infer_code)
        self.logger.info(f"avatar and item base64 encoding string : {encoding_images}")

        result_inference['encoding_image_string'] = encoding_images
        result_inference['inference_code'] = response_infer_code

        return web.json_response(result_inference)
