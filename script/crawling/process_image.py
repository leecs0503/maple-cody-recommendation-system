import json
import os
from dataclasses import asdict, dataclass
from typing import List
from urllib.request import urlretrieve

from .constant import BASE_URI_PATH
from .process_name import UserInfo, read_user_info_list
from .util import get_html_text

BASE_URL_MAPLEGG_FORMA = "https://maple.gg/u/{0}"
IMAGE_BASE_URI = os.path.join(BASE_URI_PATH, 'images')
FORMAT_IMAGE_PATH = os.path.join(IMAGE_BASE_URI, "ranking{0}_cody{1}.png")
FORMAT_JSON_PATH = os.path.join(BASE_URI_PATH, "json_data_{0}_{1}.json")


@dataclass
class UserInfoWithRecentCody(UserInfo):
    """ """
    recent_cody_list: List[str]


def _get_image_url_list_from_maplegg(user_info: UserInfo):
    """ user_info에 대해 maplegg로 부터 image_url_list를 받아오는 메소드 """
    url = BASE_URL_MAPLEGG_FORMA.format(user_info.nickname)
    soup = get_html_text(url)
    img_tag = soup.find_all(class_="character-image")[1:-1]
    return [tag["src"] for tag in img_tag]


def crawl_image_url(user_info_list: List[UserInfo]) -> List[UserInfoWithRecentCody]:
    """
    유저리스트를 받아서 각 유저에 대해 최근 코디 이미지 url들을 포함한 리스트 유저 정보를 반환하는 메소드

    Args:
        name_list (List[UserInfo]): 유저들의 (ranking, nickname)이 저장되어 있는 List

    Returns:
        List[UserInfoWithRecentCody]: (ranking, nickname, List[image_url])로 구성된 List
    """
    img_url_list = [
        _get_image_url_list_from_maplegg(user_info)
        for user_info in user_info_list
    ]

    return [
        UserInfoWithRecentCody(
            **asdict(user_info),
            recent_cody_list=recent_cody_list,
        )
        for user_info, recent_cody_list in zip(user_info_list, img_url_list)
    ]


def save_json(
    data_list: List[UserInfoWithRecentCody],
    recent_cody_uris_list: List[List[str]]
):
    """
        UserInfoWithRecentCody과 최근 저장된 uri에 맞는 json파일을 생성하고 저장하는 메소드

    Args:
        data_list             (List[UserInfoWithRecentCody]): json에 저장할 UserInfoWithRecentCody 정보
        recent_cody_uris_list (List[List[str]])             : 각 UserInfoWithRecentCody의
                                                              최근 코디 이미지가 저장된 uri들 정보.

    Returns:
        None
    """
    assert len(data_list) == len(recent_cody_uris_list)
    json_data = {
        "info": {
            "version": "v0.1.0",
            "description": "각 유저별 최근 코디가 저장되어 있는 데이터",
            "len": len(data_list)
        },
        "data": [
            {
                **asdict(data),
                "recent_cody_uris": recent_cody_uris,
            }
            for data, recent_cody_uris in zip(data_list, recent_cody_uris_list)
        ],
    }

    start_rank = data_list[0].ranking
    end_rank = data_list[-1].ranking
    with open(FORMAT_JSON_PATH.format(start_rank, end_rank), "w") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)


def save_image(user_info_list: List[UserInfoWithRecentCody]) -> List[List[str]]:
    """ process_image 함수에서 얻은 결과값을 토대로 json 파일을 생성한다. """
    uris_list = []
    os.makedirs(IMAGE_BASE_URI, exist_ok=True)
    for user_info in user_info_list:
        uris = []
        for idx, url in enumerate(user_info.recent_cody_list):
            uri = FORMAT_IMAGE_PATH.format(user_info.ranking, idx + 1)
            urlretrieve(url, uri)
            uris.append(uri)
        uris_list.append(uris)

    return uris_list


def process_image_by_user_list(user_info_list: List[UserInfo]):
    user_info_with_cody_list = crawl_image_url(user_info_list=user_info_list)
    uris_list = save_image(user_info_with_cody_list)
    save_json(
        data_list=user_info_with_cody_list,
        recent_cody_uris_list=uris_list
    )


def process_image(csv_name: str):
    user_info_list = read_user_info_list(csv_name)
    process_image_by_user_list(user_info_list)
