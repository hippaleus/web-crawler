import sys

import requests


def argumentation(BASE_URL):
    args = BASE_URL
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    return sys.argv[1]

def get_html(url: str):
    headers= {"User-Agent": "BootCrawler/1.0"}
    r = requests.get(url, headers=headers)

    if r.status_code >=400 and r.status_code < 500:
        raise Exception(f"status code: {r.status_code}")
    # print(r.headers['content-type'])
    if "text/html" not in r.headers['content-type']:
        raise Exception(f"{url} does not contain an html file")
    return r.text

def main():
    url = argumentation(sys.argv)
    print(f"starting crawl of: {url}")
    try:
        print(get_html(url))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
