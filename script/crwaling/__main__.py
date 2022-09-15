import argparse
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='크롤러')
    parser.add_argument('data_num', help='크롤링 할 데이터의 개수 지정')
    parser.add_argument('--crawl_name', action='store_true', help='캐릭터 id 크롤링')
    parser.add_argument('--crawl_image', action='store_true', help='캐릭터 코디 이미지 크롤링')
    args = parser.parse_args()

    if args.crawl_name is True:
        crawl_name(int(args.data_num))
    if args.crawl_image is True:
        crawl_image(int(args.data_num))


def crawl_name(data_num):
    PAGE_END_IDX = 11
    name_list = []
    ranking = 0

    for page in range(1, data_num + 1):
        url = f'https://maplestory.nexon.com/Ranking/World/Total?page={page}'

        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }

        html = requests.get(url, proxies=proxies).text
        soup = BeautifulSoup(html, 'html.parser')
        print(page)
        tag_list = []

        for tr_tag in soup.find(class_='rank_table').find_all('tr'):
            tag = tr_tag.find("a")
            tag_list.append(tag)

        for page_name_idx in range(1, PAGE_END_IDX):
            ranking += 1
            name_list.append([ranking, tag_list[page_name_idx].text])

    fields = ['Ranking', 'Name']

    with open('test.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(name_list)


def crawl_image(data_num):

    df = pd.read_csv('test.csv')

    for df_name_idx in range(0, data_num):
        name = df['Name'][df_name_idx]
        url = f"https://maple.gg/u/{name}"

        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }

        response = requests.get(url, proxies=proxies)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        img_tag = soup.find(class_='col-6 col-md-8 col-lg-6').find('img')

        img_url = img_tag['src']

        urllib.request.urlretrieve(img_url, f'sample{df_name_idx+1}.png')


if __name__ == '__main__':
    main()
