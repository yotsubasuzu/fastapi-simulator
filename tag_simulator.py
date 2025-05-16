import argparse
import time
from datetime import datetime

import requests

DEFAULT_TAG_IDS = ["fa451f0755d8", "fb451f0755d8", "fc451f0755d8"]


def generator(tag_ids):
    cnts = {tid: 0 for tid in tag_ids}
    while True:
        for tid in tag_ids:
            cnts[tid] += 1
            ts = datetime.now().strftime("%Y%m%d%H%M%S.%f")
            yield f"TAG,{tid},{cnts[tid]},{ts[:-3]}"
        time.sleep(5)


def output_stdout(line: str):
    print(line)


def output_file(line: str, filepath: str):
    with open(filepath, 'a') as f:
        f.write(line + '\n')


def output_socket(line: str, api_url: str):
    try:
        resp = requests.post(api_url, json={"line": line})
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to send log: {e}")


def main():
    parser = argparse.ArgumentParser(description="Tag Simulator với nhiều lựa chọn output")
    parser.add_argument("--mode", choices=["stdout", "file", "socket"], default="socket",
                        help="Chế độ xuất dữ liệu: stdout, file, socket")
    parser.add_argument("--file", type=str, default="tag.log",
                        help="Đường dẫn file cho chế độ file output")
    parser.add_argument("--api-url", type=str, default="http://localhost:8001/log",
                        help="URL endpoint cho chế độ socket")
    parser.add_argument("--tags", nargs='+', default=DEFAULT_TAG_IDS,
                        help="Danh sách Tag IDs để mô phỏng")
    args = parser.parse_args()

    sim = generator(args.tags)
    for line in sim:
        if args.mode == "stdout":
            output_stdout(line)
        elif args.mode == "file":
            output_file(line, args.file)
        else:
            output_socket(line, args.api_url)


if __name__ == "__main__":
    main()
