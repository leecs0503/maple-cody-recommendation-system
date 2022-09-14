import csv
import requests
from bs4 import BeautifulSoup


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
