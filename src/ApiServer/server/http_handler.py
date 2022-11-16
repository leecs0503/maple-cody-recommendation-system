import logging
from http import HTTPStatus

from aiohttp import web

from ..server.config import Config
import requests
from bs4 import BeautifulSoup
import json
import os


def get_html_text(url: str):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_base_wz(config) -> dict:
    cwd = os.path.dirname(os.path.realpath(__file__))
    base_wz_code_path = os.path.join(cwd, 'data', 'test_base_wz.json')
    if base_wz_code_path:
        if os.path.isfile(base_wz_code_path):
            with open(base_wz_code_path) as f:
                base_wz = json.load(f)
                return base_wz

    wcr_server_host = config.wcr_server_host
    wcr_server_port = config.wcr_server_port
    wcr_server_protocol = config.wcr_server_protocol

    url = f"{wcr_server_protocol}://{wcr_server_host}:{wcr_server_port}/code"

    res = requests.get(url, verify=False)
    base_wz = json.loads(res.text)

    if base_wz_code_path:
        with open(base_wz_code_path, "w") as f:
            json.dump(base_wz, f, ensure_ascii=False, indent="\t")

    return base_wz


def get_avatar_item_encoding_string(item_code: dict) -> dict:
    wz_server_url = 'https://0.0.0.0:7209/avatar'
    obj = {}
    encoding_images = {}

    for key, value in item_code.items():
        if key == 'skin':
            key = 'head'
        if key == 'shield':
            continue
        if value == '0':
            continue
        if key == 'name':
            continue
        obj[key] = value
    obj['bs'] = 'true'

    for key, value in obj.items():
        if key == 'bs':
            continue
        item_image_url = f'https://0.0.0.0:7209/{key}/?code={value}&bs=true'
        res = requests.get(item_image_url, verify=False)
        encoding_images[key] = res.text
    res = requests.get(wz_server_url, params=obj, verify=False)
    encoding_images['avatar'] = res.text

    return encoding_images


def get_item_code_name(base_wz: dict , item_code: dict) -> dict:
    item_code_name = {}
    for key , value in item_code.items():
        if value == '0':
            continue
        if key == 'hair':
            value = value.split('+')[0]
            item_code_name[key] = base_wz[key][value]['name']
            continue
        if key == 'skin':
            key = 'head'
            item_code_name[key] = base_wz[key][item_code['skin']]['name']
            continue
        if key == 'shield':
            continue
        item_code_name[key] = base_wz[key][item_code[key]]['name']
    return item_code_name


class HttpHandler:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ):
        self.logger = logger
        self.config = config

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
        avatar_server_url = "http://localhost:8080/packed_character_look"

        post = await request.text()
        post = json.loads(post)
        self.logger.info(f"web server character request information: {post}")
        res = post['name']

        maple_gg_url = f'https://maple.gg/u/{res}'

        soup = get_html_text(maple_gg_url)

        img_tag = soup.find_all(class_="character-image")[1]["src"]
        self.logger.info(f"crawling character url : {img_tag}")

        encrypted_code = img_tag.replace('https://avatar.maplestory.nexon.com/Character/', '').replace('.png', '')
        response = requests.post(avatar_server_url, json={"packed_character_look": encrypted_code})
        self.logger.info(f"web server character code response: {response.text}")

        return web.Response(body=response.text, status=HTTPStatus.OK)

    async def infer_code_web_handler(self, request: web.Request) -> web.json_response:
        result_inference = {}

        post = await request.text()
        post = json.loads(post)
        post = post["character_code_result"]
        self.logger.info(f"inference request text : {post}")

        # response = requests.post("http://localhost:8080/inference", post)  -> infer 서버에 사용자의 코드 요청
        # 추천된 코드를 json으로 저장하여 response로 받는다고 가정

        response_infer_code = '{"face": "54002", "cap": "1005041", "longcoat": "1053240", "weapon": "1703048", "cape": "1103332", "coat": "0", "glove": "1082703", "hair": "61481+3*50", "pants": "0", "shield": "1092067", "shoes": "1073534", "faceAccessory": "1012050", "eyeAccessory": "1022079", "earrings": "1032022", "skin": "12024"}'
        response_infer_code = json.loads(response_infer_code)
        self.logger.debug(f"inference character code : {response_infer_code}")

        encoding_images_string = get_avatar_item_encoding_string(item_code=response_infer_code)
        self.logger.info(f"avatar and item base64 encoding string : {encoding_images_string}")
        base_wz = get_base_wz(self.config)
        self.logger.info(f"base_wz_code keys: {base_wz.keys()}")

        item_code_name = get_item_code_name(base_wz=base_wz, item_code=response_infer_code)
        self.logger.info(f"inference item_code_name : {item_code_name}")

        result_inference['encoding_image_string'] = encoding_images_string
        result_inference['infer_item_code_name'] = item_code_name

        return web.json_response(result_inference)
