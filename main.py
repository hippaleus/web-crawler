import asyncio
import sys
from asyncio.tasks import create_task
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
            return await response.text()

    async def page_crawl(self, base_url:str, current_url=None, page_data=None):
        # if self.page_data is None:
        #     page_data = {}
        if current_url is None:
            current_url = base_url
        if urlsplit(current_url).netloc != urlsplit(base_url).netloc:
            return

        normalized = crawl.normalize_url(current_url)
        if normalized in self.page_data:
            return self.page_data

        visit = self.add_page_visit(normalized)
        visited = await visit
        if visited is False:
            return
        async with self.semaphore:
            getting = self.get_html(current_url)
            html = await getting

            print(f"crawling: {current_url}")

            data = crawl.extract_page_data(html, current_url)
            self.page_data[normalized] = data

        tasks = []
        for link in data["outgoing_links"]:
            full_url = urljoin(base_url, link)
            task = asyncio.create_task(self.page_crawl(base_url, full_url, self.page_data))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def crawl(self):
        await self.page_crawl(self.base_url)
        return self.page_data


async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url) as c:
        return await c.crawl()


def argumentation(BASE_URL):
    args = BASE_URL
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    return sys.argv[1]


async def main():
    base_url = argumentation(sys.argv)
    print(f"starting crawl of: {base_url}")
    page_data = await crawl_site_async(base_url)
    for page in page_data.values():
        print(page["url"])
        print(page["heading"])

if __name__ == "__main__":
    asyncio.run(main())
