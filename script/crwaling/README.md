# crawler
> 메이플 공식 홈페이지의 유저 id와 maple.gg 사이트의 유저 id에 대한 코디 이미지를 크롤링 합니다.



## 사용법


- 메이플 공식 홈페이지 유저 id 크롤링:
> python \_\_main\_\_.py --start_page_idx 1 --num_want_to_crawl 10 --crawl_name

start_page_idx는 크롤링을 시작할 페이지 index이고, num_want_to_crawl은 크롤링 할 페이지 개수 입니다.

- maple.gg 사이트의 코디 이미지 크롤링:
> python \_\_main\_\_.py --crawl_image

메이플 공식 홈페이지에서 크롤링 한 결과가 csv 형태로 저장되고 이를 활용하여 이미지를 크롤링 합니다.


