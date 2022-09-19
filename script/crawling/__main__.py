import argparse

from .process_image import process_image, process_image_by_user_list
from .process_name import process_name


def main():
    parser = argparse.ArgumentParser(description="크롤러")
    parser.add_argument("--start-page-idx", type=int, help="크롤링 할 페이지 시작 지점 지정")
    parser.add_argument("--end-page-idx", type=int, help="크롤링 할 페이지 마지막 지점 지정")
    parser.add_argument("--csv-name", type=str, help="이미지 크롤링 할 csv 파일 지정")
    parser.add_argument("--json-name", nargs="*", help="merge 할 json 파일 지정(원하는 만큼 적어주어야 한다)")
    parser.add_argument("--crawl-name", action="store_true", help="캐릭터 id 크롤링")
    parser.add_argument("--crawl-image", action="store_true", help="캐릭터 코디 이미지 크롤링")
    parser.add_argument("--json-merge", action="store_true", help="json_merge")

    args = parser.parse_args()

    if args.crawl_name and args.crawl_image:
        user_info_list = process_name(args.start_page_idx, args.end_page_idx)
        process_image_by_user_list(user_info_list)
    else:
        if args.crawl_name:
            process_name(args.start_page_idx, args.end_page_idx)
        if args.crawl_image:
            process_image(args.csv_name)

    # if args.json_merge:
    #     json_merge(args.json_name)


if __name__ == "__main__":
    main()
