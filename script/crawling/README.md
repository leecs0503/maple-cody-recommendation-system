# crawler
> 메이플 공식 홈페이지의 유저 id와 maple.gg 사이트의 유저 id에 대한 코디 이미지를 크롤링 합니다.

## tor
> sudo apt-get install tor
> sudo apt-get install torsocks

## tor test
in terminal1
> bash tor.sh
in terminal2
> torsocks curl https://google.co.kr



## 사용법


- 메이플 공식 홈페이지 유저 id 크롤링:
> python -m script.crawling --crawl-name --crawl-image --start-page-idx=1 --end-page-idx=1

start_page_idx는 크롤링을 시작할 페이지 index이고, num_want_to_crawl은 크롤링 할 페이지 개수 입니다.

- maple.gg 사이트의 코디 이미지 크롤링:
> python \_\_main\_\_.py --csv_name 2_3_page_user_id --crawl_image

메이플 공식 홈페이지에서 크롤링 한 결과가 csv 형태로 저장되고 원하는 csv 파일을 지정하여 이미지를 크롤링 합니다.

- json 파일 병합:
> python \_\_main\_\_.py --json_name json_data_11_30 json_data_31_50 --json_merge

json 파일 명을 지정하여 병합을 진행합니다.(복수 개 지정 가능)
