import csv
import json
import urllib

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

    Keyword arguments:
    num_want_to_crawl -- 크롤링 하고 싶은 유저 id 개수
    start_page_idx -- 크롤링을 진행 할 page idx
    NUM_OF_CHARACTER_IN_ONE_PAGE -- 한 페이지 당 id 개수
    name_list -- 전체 유저 id 데이터를 담을 list
    tag_list -- 한 페이지 내의 유저 id 데이터를 담을 list
    ranking -- 유저의 ranking 데이터
    fields -- 생성할 csv 파일의 column 이름
    """

    NUM_OF_CHARACTER_IN_ONE_PAGE = 10
    name_list = []

    for page in range(start_page_idx, start_page_idx + num_want_to_crawl):
        ranking = (page - 1) * 10
        url = BASE_URL_MAPLE_OFFICIAL + f"?page={page}"
        soup = get_html_text(url)

        rank_table = soup.find(class_="rank_table")
        assert isinstance(rank_table, Tag), "해당 class의 Tag가 없습니다. class 명을 확인해 주세요"
        tag_list = [tr_tag.find("a") for tr_tag in rank_table.find_all("tr") if isinstance(tr_tag, Tag)]
        assert len(tag_list) > 0, "tag_list가 비었습니다."

        for page_name_idx in range(1, NUM_OF_CHARACTER_IN_ONE_PAGE + 1):
            ranking += 1
            name_list.append((ranking, tag_list[page_name_idx].text))

    fields = ["Ranking", "Name"]

    with open(f"{start_page_idx}_{start_page_idx + num_want_to_crawl - 1}_page_user_id.csv", "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(name_list)


def crawl_image(csv_name: str):
    """사이트 내에 있는 유저 코디 이미지 데이터를 크롤링 한다.

    maple.gg 사이트에서 html을 받아와 이미지에 해당하는 url을 저장 한 뒤, 다운로드를 진행한다.
    crawl_name 함수에서 얻은 csv 데이터 파일의 name column을 활용해
    반복문을 이용하여 page를 바꿔가면서 크롤링 진행한다.

    Keyword arguments:
    df -- crawl_name 함수에서 얻은 csv 파일에 대한 데이터 프레임
    name -- 유저 id
    rank -- 유저 ranking
    csv_name -- 크롤링 하고 싶은 csv 파일(입력으로 받는다)
    img_tag -- 사이트 내에 있는 이미지 tag의 html
    img_url -- image 태그 안에 있는 이미지 url
    """
    RECENT_CODY_NUM = 6

    df = pd.read_csv(f"{csv_name}.csv")
    RANK_START = df["Ranking"][0]

    json_data = {}
    json_data["info"] = []

    for df_name_idx in range(0, len(df["Name"])):
        name = df["Name"][df_name_idx]
        rank = df["Ranking"][df_name_idx]
        url = BASE_URL_MAPLEGG + f"/{name}"
        soup = get_html_text(url)

        img_tag = soup.find_all(class_="character-image")
        img_tag.pop(0)
        img_tag.pop()
        for recent_cody in range(RECENT_CODY_NUM):
            img_url = img_tag[recent_cody]["src"]
            urllib.request.urlretrieve(img_url, f"ranking{rank}_cody{recent_cody + 1}.png")

        data = {
            "name": f"{name}",
            "ranking": f"{rank}",
            "img_url_1": f"./ranking{rank}_cody1.png",
            "img_url_2": f"./ranking{rank}_cody2.png",
            "img_url_3": f"./ranking{rank}_cody3.png",
            "img_url_4": f"./ranking{rank}_cody4.png",
            "img_url_5": f"./ranking{rank}_cody5.png",
            "img_url_6": f"./ranking{rank}_cody6.png",
        }

        json_data["info"].append(data)

    with open(f"json_data_{RANK_START}_{rank}.json", "w") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)


def json_merge(json_name_1: str, json_name_2: str):

    NAME_START_IDX = json_name_1[10:12]
    NAME_END_IDX = json_name_2[13:15]

    with open(f"./{json_name_1}.json") as file_1:
        data1 = json.load(file_1)

    with open(f"./{json_name_2}.json") as file_2:
        data2 = json.load(file_2)

    for json_idx in range(0, len(data2["info"])):
        data1["info"].append(data2["info"][json_idx])

    with open(f"json_data_{NAME_START_IDX}_{NAME_END_IDX}.json", "w") as f:
        json.dump(data1, f, indent=2, ensure_ascii=False)
