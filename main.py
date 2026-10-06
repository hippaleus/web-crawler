import asyncio
import sys
from multiprocessing import Semaphore
from urllib.parse import urlsplit

import aiohttp
from requests.compat import urljoin

import crawl


class AsyncCrawler:
    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited =  set()
        self.lock = asyncio.Lock()
        self.max_concurrency = 2
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tp):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.visited:
                return False
            else:
                self.visited.add(normalized_url)
                return True
    async def get_html(self, url: str):
        headers= {"User-Agent": "BootCrawler/1.0"}
        async with self.session.get(url, headers=headers) as response:

            if response.status >=400 and response.status < 500:
                raise Exception(f"status code: {response.status}")
            # print(r.headers['content-type'])
            if "text/html" not in response.headers['content-type']:
                raise Exception(f"{url} does not contain an html file")
            return response.text

def argumentation(BASE_URL):
    args = BASE_URL
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    return sys.argv[1]

# def get_html(url: str):
#     headers= {"User-Agent": "BootCrawler/1.0"}
#     r = requests.get(url, headers=headers)
#
#     if r.status_code >=400 and r.status_code < 500:
#         raise Exception(f"status code: {r.status_code}")
#     # print(r.headers['content-type'])
#     if "text/html" not in r.headers['content-type']:
#         raise Exception(f"{url} does not contain an html file")
#     return r.text
#

def page_crawl(base_url:str, current_url=None, page_data=None):
    if page_data is None:
        page_data = {}
    if urlsplit(current_url).netloc != urlsplit(base_url).netloc:
       return
    normalized = crawl.normalize_url(current_url)
    if normalized in page_data:
        return page_data
    html = get_html(current_url)
    print(f"crawling: {current_url}")
    data = crawl.extract_page_data(html, base_url)
    page_data[normalized] = data

    for link in data["outgoing_links"]:
        full_url = urljoin(base_url, link)
        page_crawl(base_url, full_url, page_data)

    return page_data

def main():
    url = argumentation(sys.argv)
    print(f"starting crawl of: {url}")
    try:
        (get_html(url))
    except Exception as e:
        print(f"Error: {e}")

    page_crawl(url, url)

if __name__ == "__main__":
    main()
