import argparse

from crawl import crawl_image, crawl_name


def main():
    parser = argparse.ArgumentParser(description="크롤러")
    parser.add_argument("--num_want_to_crawl", type=int, help="크롤링 할 데이터의 개수 지정")
    parser.add_argument("--start_page_idx", type=int, help="크롤링 할 페이지 시작 지점 지정")
    parser.add_argument("--crawl_name", action="store_true", help="캐릭터 id 크롤링")
    parser.add_argument("--crawl_image", action="store_true", help="캐릭터 코디 이미지 크롤링")
    args = parser.parse_args()

    if args.crawl_name:
        crawl_name(args.start_page_idx, args.num_want_to_crawl)
    if args.crawl_image:
        crawl_image()


if __name__ == "__main__":
    main()
