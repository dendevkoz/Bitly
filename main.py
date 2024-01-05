import requests
import os
from dotenv import load_dotenv
import argparse


def shorten_link(long_url, headers):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    payload = {"long_url": long_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()["id"]
    return bitlink


def count_clicks(bitlink, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(user_url, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{user_url}"
    response = requests.get(url, headers=headers)
    return response.ok


def main(user_url):
    load_dotenv()
    headers = {"Authorization": f"Bearer {os.getenv('BITLY_KEY', default=None)}"}
    if is_bitlink(user_url, headers):
        try:
            print("По вашей ссылке прошли", count_clicks(user_url, headers), "раз(а)")
        except requests.exceptions.HTTPError:
            print("Введена некорректная сокращенная ссылка")
    else:
        try:
            print("Битлинк", shorten_link(user_url, headers))
        except requests.exceptions.HTTPError:
            print("Введена неверная ссылка")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_url", type=str, help="The program works with this site")
    args = parser.parse_args()
    main(args.user_url)
