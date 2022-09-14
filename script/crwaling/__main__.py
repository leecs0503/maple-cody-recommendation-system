import argparse
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='크롤러')

    parser.add_argument('--name', action='store_true')
    parser.add_argument('--image', action='store_true')
    args = parser.parse_args()

    if args.name is True:
        name()
    if args.image is True:
        image()


def name():
    name_list = []
    i = 0

    for page in range(1, 101):
        url = f'https://maplestory.nexon.com/Ranking/World/Total?page={page}'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        tag_list = []

        for tr_tag in soup.find(class_='rank_table').find_all('tr'):
            tag = tr_tag.find("a")
            tag_list.append(tag)

        for j in range(1, 11):
            i += 1
            name_list.append([i, tag_list[j].text])

    fields = ['Ranking', 'Name']

    with open('test.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(name_list)


def image():
    df = pd.read_csv('1test.csv')

    for i in range(0, 99):
        name = df['Name'][i]
        url = f"https://maple.gg/u/{name}"

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        tr_tag = soup.find(class_='col-6 col-md-8 col-lg-6').find('img')

        download = tr_tag['src']

        urllib.request.urlretrieve(download, f'sample{i+1}.png')


main()
