import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pandas as pd


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
