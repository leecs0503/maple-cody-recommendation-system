import argparse

from crawl import crawl_image, crawl_name, json_merge


def main():
    parser = argparse.ArgumentParser(description="크롤러")
    parser.add_argument("--num_want_to_crawl", type=int, help="크롤링 할 데이터의 개수 지정")
    parser.add_argument("--start_page_idx", type=int, help="크롤링 할 페이지 시작 지점 지정")
    parser.add_argument("--csv_name", type=str, help="이미지 크롤링 할 csv 파일 지정")
    parser.add_argument("--json_name", nargs="*", help="merge 할 json 파일 지정(원하는 만큼 적어주어야 한다)")
    parser.add_argument("--crawl_name", action="store_true", help="캐릭터 id 크롤링")
    parser.add_argument("--crawl_image", action="store_true", help="캐릭터 코디 이미지 크롤링")
    parser.add_argument("--json_merge", action="store_true", help="json_merge")

    args = parser.parse_args()

    if args.crawl_name:
        crawl_name(args.start_page_idx, args.num_want_to_crawl)
    if args.crawl_image:
        crawl_image(args.csv_name)
    if args.json_merge:
        json_merge(args.json_name)


if __name__ == "__main__":
    main()
