import argparse
import csv
import urllib.request

import pandas as pd
import requests
from bs4 import BeautifulSoup

proxies = {"http": "socks5://0.0.0.0:9050", "https": "socks5://0.0.0.0:9050"}


def main():
    parser = argparse.ArgumentParser(description="크롤러")
    parser.add_argument("--num_want_to_crawl", type=int, help="크롤링 할 데이터의 개수 지정")
    parser.add_argument("--crawl_name", action="store_true", help="캐릭터 id 크롤링")
    parser.add_argument("--crawl_image", action="store_true", help="캐릭터 코디 이미지 크롤링")
    args = parser.parse_args()

    if args.crawl_name:
        crawl_name(args.num_want_to_crawl)
    if args.crawl_image:
        crawl_image(args.num_want_to_crawl)


def crawl_name(num_want_to_crawl: int):
    NUM_OF_CHARACTER_IN_ONE_PAGE = 11
    name_list = []
    ranking = 0

    for page in range(1, num_want_to_crawl + 1):
        url = f"https://maplestory.nexon.com/Ranking/World/Total?page={page}"
        html = requests.get(url, proxies=proxies).text
        soup = BeautifulSoup(html, "html.parser")

        tag_list = [tr_tag.find("a") for tr_tag in soup.find(class_="rank_table").find_all("tr")]

        for page_name_idx in range(1, NUM_OF_CHARACTER_IN_ONE_PAGE):
            ranking += 1
            name_list.append((ranking, tag_list[page_name_idx].text))

    fields = ["Ranking", "Name"]

    with open("test.csv", "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(name_list)


def crawl_image(num_want_to_crawl: int):

    df = pd.read_csv("test.csv")

    for df_name_idx in range(0, num_want_to_crawl):
        name = df["Name"][df_name_idx]
        url = f"https://maple.gg/u/{name}"

        response = requests.get(url, proxies=proxies)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        img_tag = soup.find(class_="col-6 col-md-8 col-lg-6").find("img")

        img_url = img_tag["src"]

        urllib.request.urlretrieve(img_url, f"sample{df_name_idx+1}.png")


if __name__ == "__main__":
    main()
