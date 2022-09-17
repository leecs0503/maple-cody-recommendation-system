import csv
import json
import urllib
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

_PROXIES = {"http": "socks5://0.0.0.0:9050", "https": "socks5://0.0.0.0:9050"}

BASE_URL_MAPLE_OFFICIAL = "https://maplestory.nexon.com/Ranking/World/Total"
BASE_URL_MAPLE_OFFICIAL_FORMA = "https://maplestory.nexon.com/Ranking/World/Total?page={0}"

BASE_URL_MAPLEGG = "https://maple.gg/u"


def get_html_text(url: str):
    html = requests.get(url, proxies=_PROXIES).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def crawl_name(start_page_idx: int, num_want_to_crawl: int):
    """사이트 내에 있는 유저 id 데이터를 크롤링 한다.

    메이플 공식 사이트에서 html을 받아와 id에 해당하는 정보를 list에 담는다.
    한 페이지 당 10개의 id가 있으므로 반복문을 이용하여 page를 바꿔가면서 크롤링 진행한다.

    arguments:
    num_want_to_crawl -- 크롤링 하고 싶은 유저 id 개수
    start_page_idx -- 크롤링을 진행 할 page idx


    """

    NUM_OF_CHARACTER_IN_ONE_PAGE = 10
    name_list = []

    for page in range(start_page_idx, start_page_idx + num_want_to_crawl):
        ranking = (page - 1) * 10
        url = BASE_URL_MAPLE_OFFICIAL + f"?page={page}"
        soup = get_html_text(url)

        rank_table = soup.find(class_="rank_table")
        assert isinstance(rank_table, Tag), "crawl_name method_해당 class의 Tag가 없습니다. class 명을 확인해 주세요"
        tag_list = [tr_tag.find("a") for tr_tag in rank_table.find_all("tr") if isinstance(tr_tag, Tag)]
        assert len(tag_list) > 0, "crawl_name method_tag_list가 비었습니다. 해당 class의 tr Tag가 없습니다. 태그 명을 다시 확인 해 주세요"

        for page_name_idx in range(1, NUM_OF_CHARACTER_IN_ONE_PAGE + 1):
            ranking += 1
            name_list.append((ranking, tag_list[page_name_idx].text))

    fields = ["Ranking", "Name"]

    with open(f"{start_page_idx}_{start_page_idx + num_want_to_crawl - 1}_page_user_id.csv", "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(name_list)


def process_image(csv_name: str):
    """사이트 내에 있는 유저 코디 이미지 데이터를 크롤링 한다.

    maple.gg 사이트에서 html을 받아와 이미지에 해당하는 url을 저장 한 뒤, 다운로드를 진행한다.
    crawl_name 함수에서 얻은 csv 데이터 파일의 name column을 활용해
    반복문을 이용하여 page를 바꿔가면서 크롤링 진행한다.

    arguments:
    csv_name -- 이미지 크롤링 하고자 하는 유저의 id 정보와 ranking 정보가 들어있는 csv 파일의 csv 이름


    """
    NUM_RECENT_CODY = 6

    df = pd.read_csv(f"{csv_name}.csv")
    rank_start = df["Ranking"][0]
    num_data_csv = len(df["Name"])
    img_url_list = []

    for df_name_idx in range(0, num_data_csv):
        name = df["Name"][df_name_idx]
        url = BASE_URL_MAPLEGG + f"/{name}"
        soup = get_html_text(url)

        img_tag = soup.find_all(class_="character-image")[1:-1]

        for recent_cody in range(NUM_RECENT_CODY):
            img_url = img_tag[recent_cody]["src"]
            img_url_list.append(img_url)

    json_save(list(df["Name"]), list(df["Ranking"]), num_data_csv, rank_start, NUM_RECENT_CODY)
    image_save(img_url_list, num_data_csv, rank_start, NUM_RECENT_CODY)


def json_save(name_list: list, ranking_list: list, num_data_csv: int, rank_start: int, NUM_RECENT_CODY: int):
    """process_image 함수에서 얻은 결과값을 토대로 json 파일을 생성한다.


    arguments:
    name_list -- 유저 id 정보를 담고 있는 list
    ranking_list -- 유저 랭킹 정보를 담고 있는 list
    num_data_csv -- csv 파일의 총 길이
    rank_start -- csv 파일의 유저 ranking의 시작 ranking
    NUM_RECENT_CODY -- 한 페이지 당 최근 코디 이미지 개수


    """

    json_data = {
        "info": [],
    }

    for df_name_idx in range(0, num_data_csv):
        name = name_list[df_name_idx]
        rank = ranking_list[df_name_idx]
        data = {
            "name": f"{name}",
            "ranking": f"{rank}",
        }
        for img_url_idx in range(1, NUM_RECENT_CODY + 1):
            data[f"img_url_{img_url_idx}"] = f"./ranking{rank}_cody{img_url_idx}.png"

        json_data["info"].append(data)

    with open(f"json_data_{rank_start}_{rank}.json", "w") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)


def image_save(img_url_list: List[str], num_data_csv: int, rank_start: int, NUM_RECENT_CODY: int):
    """process_image 함수에서 얻은 결과값을 토대로 json 파일을 생성한다.


    arguments:
    img_url_list -- 크롤링 한 image의 url 정보를 담고 있는 list
    num_data_csv -- csv 파일의 총 길이
    rank_start -- csv 파일의 유저 ranking의 시작 ranking
    NUM_RECENT_CODY -- 한 페이지 당 최근 코디 이미지 개수


    """

    for rank in range(0, num_data_csv):
        for num_cody in range(0, NUM_RECENT_CODY):
            urllib.request.urlretrieve(
                img_url_list[(NUM_RECENT_CODY * rank) + num_cody], f"ranking{rank_start}_cody{num_cody + 1}.png"
            )
        rank_start += 1


def file_load(json_file_idx: str):
    with open(f"./{json_file_idx}.json") as f:
        json_data = json.load(f)
    return json_data


def json_merge(json_name: list):

    NAME_START_IDX = json_name[0][10:12]  # 10:12 는 입력 된 json_name의 시작 ranking에 해당하는 숫자를 슬라이싱 한 것
    NAME_END_IDX = json_name[-1][13:15]  # 13:15는 입력 된 json_name의 마지막 ranking에 해당하는 숫자를 슬라이싱 한 것

    total_json_data = {
        "info": [],
    }

    for file_idx in range(len(json_name)):
        json_file = file_load(json_name[file_idx])
        for info_idx in range(0, len(json_file["info"])):
            total_json_data["info"].append(json_file["info"][info_idx])

    with open(f"json_data_{NAME_START_IDX}_{NAME_END_IDX}.json", "w") as f:
        json.dump(total_json_data, f, indent=2, ensure_ascii=False)
