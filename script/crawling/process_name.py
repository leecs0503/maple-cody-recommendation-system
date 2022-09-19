import csv
import logging
import os
from dataclasses import dataclass
from typing import List

import pandas as pd
from bs4.element import Tag

from .constant import BASE_URI_PATH
from .util import get_html_text

logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)

BASE_URL_MAPLE_OFFICIAL_FORMA = "https://maplestory.nexon.com/Ranking/World/Total?page={0}"
FORMAT_NAME_LIST = os.path.join(BASE_URI_PATH, "user_info_{0}_{1}.csv")


@dataclass
class UserInfo:
    """ 유저 정보 """
    ranking: int
    nickname: str


def _get_name_list_from_maple_ranking_site(page_num: int) -> List[str]:
    """ 메이플 공식 홈페이지 랭킹 page_num 페이지에서 유저 정보가 들어있는 tag_list를 반환 """
    url = BASE_URL_MAPLE_OFFICIAL_FORMA.format(page_num)
    soup = get_html_text(url)

    rank_table = soup.find(class_="rank_table")
    assert isinstance(rank_table, Tag), "crawl_name: method_해당 class의 Tag가 없습니다. class 명을 확인해 주세요"
    tag_list = [tr_tag.find("a") for tr_tag in rank_table.find_all("tr") if isinstance(tr_tag, Tag)]
    assert len(tag_list) > 0, "crawl_name: method_tag_list가 비었습니다. 해당 class의 tr Tag가 없습니다. 태그 명을 다시 확인 해 주세요"

    # soup가 반환하는 객체는 1-based List (tag_list[0] = None)
    name_list = [tag.text for idx, tag in enumerate(tag_list) if idx != 0 and tag is not None]

    return name_list


def crawl_name(start_page_idx: int, last_page_idx: int) -> List[UserInfo]:
    """
    메이플 공식 사이트로부터 유저 id를 크롤링해서,
    유저들의 (랭킹, 닉네임)을 반환하는 메소드.

    Args:
        start_page_idx    (int): 크롤링을 진행할 시작 page 번호.
        last_page_idx     (int): 크롤링을 진행할 끝 page 번호.

    Returns:
        List[UserInfo]: 크롤링된 유저들의 유저 정보 (랭킹, 닉네임) 리스트

    Examples:
        >>> crwal_name(2, 3)
        [(20, "닉네임x"), (21, "닉네임y"), ..., (39, "닉네임zz")] # 20개
    """
    NUM_OF_CHARACTER_IN_ONE_PAGE = 10

    user_info_list = []
    for page_num in range(start_page_idx, last_page_idx + 1):
        name_list = _get_name_list_from_maple_ranking_site(page_num=page_num)

        start_ranking = (page_num - 1) * NUM_OF_CHARACTER_IN_ONE_PAGE + 1
        user_info_list += [
            UserInfo(
                ranking=start_ranking + idx,
                nickname=name,
            )
            for idx, name in enumerate(name_list)
        ]

    return user_info_list


def save_user_info_list(user_info_list: List[UserInfo]) -> None:
    """ user_info_list(List[UserInfo])를 저장하는 메소드 """

    fields = ["Ranking", "Name"]
    first_ranking = user_info_list[0].ranking
    last_ranking = user_info_list[-1].ranking

    with open(FORMAT_NAME_LIST.format(first_ranking, last_ranking), "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows([
            (
                user_info.ranking,
                user_info.nickname
            )
            for user_info in user_info_list
        ])


def read_user_info_list(csv_name: str) -> List[UserInfo]:
    """ csv파일을 읽어서 user_info_list를 반환하는 메소드 """
    df = pd.read_csv(f"{csv_name}.csv")
    return [
        UserInfo(ranking=ranking, nickname=name)
        for ranking, name in zip(df["Ranking"], df["Name"])
    ]


def process_name(start_page_idx: int, end_page_idx: int):
    logger.info(f"process name start! st: {start_page_idx}, en: {end_page_idx}")
    user_info_list = crawl_name(start_page_idx, end_page_idx)
    save_user_info_list(user_info_list)
    logger.info(f"process name end! len(user_info_list): {len(user_info_list)}")
    return user_info_list
