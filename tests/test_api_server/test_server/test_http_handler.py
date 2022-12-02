import pytest
from aiohttp.test_utils import make_mocked_request
from src.ApiServer.server.http_handler import HttpHandler
from tests.test_api_server.util.make_mocked_request import _make_mocked_request_json
import requests_mock
import os
import json


@pytest.mark.asyncio
async def test_http_index_handler(test_http_handler: HttpHandler):
    request = make_mocked_request("GET", "/")
    result = await test_http_handler.index_handler(request=request)
    assert result.status == 200


@pytest.mark.asyncio
async def test_http_healthcheck_handler(test_http_handler: HttpHandler):
    request = make_mocked_request("GET", "/healthcheck")
    result = await test_http_handler.healthcheck_handler(request=request)
    assert result.status == 200


@pytest.mark.asyncio
async def test_character_code_web_handler(test_http_handler: HttpHandler):
    MOCKED_MAPLE_GG_URL = "https://maple.gg/u/Nine"
    MOCKED_AVATAR_SERVER_URL = "http://localhost:8080/packed_character_look"

    cwd = os.path.dirname(os.path.realpath(__file__))
    html_text_path = os.path.join(cwd, "test_data", "maple_gg_html_response.txt")
    character_result_code_path = os.path.join(cwd, "test_data", "character_result_code.txt")

    with requests_mock.mock() as m:
        html_file = open(html_text_path, encoding="utf8")
        html_text = html_file.read()

        m.get(MOCKED_MAPLE_GG_URL, text=html_text)
        m.post(
            MOCKED_AVATAR_SERVER_URL,
            json={
                "face": "28172",
                "cap": "1005842",
                "longcoat": "1051673",
                "weapon": "1703129",
                "cape": "1102039",
                "coat": "0",
                "glove": "1082102",
                "hair": "61194+6*62",
                "pants": "0",
                "shield": "1092067",
                "shoes": "1072153",
                "faceAccessory": "1012719",
                "eyeAccessory": "1022079",
                "earrings": "1032024",
                "skin": "12016",
            },
        )

        request = _make_mocked_request_json(obj={"name": "Nine"}, request_path="/test_character_code_web_handler")

        result = await test_http_handler.character_code_web_handler(request=request)

        character_result_code_file = open(character_result_code_path, encoding="utf8")
        character_result_code_text = character_result_code_file.read()

        assert result.text == character_result_code_text


@pytest.mark.asyncio
async def test_infer_code_web_handler(test_http_handler: HttpHandler):
    MOCKERD_AVATAR_URL = "http://localhost:8080/avatar_image"

    cwd = os.path.dirname(os.path.realpath(__file__))
    bs64_character_string_path = os.path.join(cwd, "test_data", "bs64_character_string.txt")
    infer_result_path = os.path.join(cwd, "test_data", "infer_result.txt")

    with requests_mock.mock() as m:
        bs64_string_file = open(bs64_character_string_path, encoding="utf8")
        bs64_string_text = bs64_string_file.read()

        m.post(
            MOCKERD_AVATAR_URL,
            text=bs64_string_text,
        )
        request = _make_mocked_request_json(
            obj={
                "character_code_result": {
                    "face": "28172",
                    "cap": "1005842",
                    "longcoat": "1051673",
                    "weapon": "1703129",
                    "cape": "1102039",
                    "coat": "0",
                    "glove": "1082102",
                    "hair": "61194+6*62",
                    "pants": "0",
                    "shield": "1092067",
                    "shoes": "1072153",
                    "faceAccessory": "1012719",
                    "eyeAccessory": "1022079",
                    "earrings": "1032024",
                    "skin": "12016",
                }
            },
            request_path="/infer_code_web_handler",
        )

        result = await test_http_handler.infer_code_web_handler(request=request)

        infer_result_file = open(infer_result_path, encoding="utf8")
        result_code_text = infer_result_file.read()

        assert result.text == result_code_text

@pytest.mark.asyncio
async def test_recommend_handler(test_http_handler: HttpHandler):
    cwd = os.path.dirname(__file__)
    json_path = os.path.join(cwd, 'test_data', 'test_recommend_data.json')
    with open(json_path, 'rt') as file:
        data = json.load(file)
    request = _make_mocked_request_json(
        obj={
            "encrypted_character_image": data["encrypted_character_image"],
            "parts_to_change": data["parts_to_change"],
        },
        request_path="/recommend",
    )

    result = await test_http_handler.recommend_handler(request=request)

    assert result.text == "avatar image"