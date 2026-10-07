import asyncio
import sys
from asyncio.tasks import create_task
from multiprocessing import Semaphore
from urllib.parse import urlsplit

import aiohttp
from requests.compat import urljoin

import crawl


class AsyncCrawler:
    def __init__(self, base_url, max_pages, max_concurrency) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited =  set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = bool
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tp):
        await self.session.close()  # pyright: ignore[reportOptionalMemberAccess]

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop is True:
                return False


            if self.max_pages is not None and len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum amount of pages to crawl")
                return False

            if normalized_url in self.visited:
                return False
            else:
                self.visited.add(normalized_url)
                return True
    async def get_html(self, url: str):
        headers= {"User-Agent": "BootCrawler/1.0"}
        async with self.session.get(url, headers=headers) as response:  # pyright: ignore[reportOptionalMemberAccess]

            if response.status >=400 and response.status < 500:
                raise Exception(f"status code: {response.status}")
            if "text/html" not in response.headers['content-type']:
                raise Exception(f"{url} does not contain an html file")
            return await response.text()

    async def page_crawl(self, base_url:str, current_url=None, page_data=None):
        if self.should_stop is True:
            return
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


async def crawl_site_async(base_url, max_pages, max_concurrency):
    async with AsyncCrawler(base_url, max_pages, max_concurrency) as c:
        return await c.crawl()


def argumentation(args):
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)

    url = args[1]
    max_pages = None
    max_concurrency = 2
    if len(args) >= 3:
         max_concurrency = int(args[2])
    if len(args) >= 4:
        max_pages = int(args[3])


    if len(args) > 4:
        print("too many arguments provided")
        sys.exit(1)
    return url, max_pages, max_concurrency


async def main():
    base_url, max_pages, max_concurrency = argumentation(sys.argv)
    print(f"starting crawl of: {base_url}")
    page_data = await crawl_site_async(base_url, max_pages, max_concurrency)
    for page in page_data.values():
        print(page["url"])
        print(page["heading"])

if __name__ == "__main__":
    asyncio.run(main())
