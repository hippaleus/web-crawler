from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup, Tag
from typing_extensions import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]



def normalize_url(url:str) -> str:
    split = urlsplit(url)
    # first = split._replace(netloc="boot.dev").geturl()
    # second: str = split._replace(scheme="http").geturl()
    # third: str = split._replace(fragment="").geturl()
    # fourth: str = split._replace(path="pricing").geturl()
    # fifth: str = split._replace(scheme="").geturl()
    return f"{split.netloc}{split.path}"

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    header = soup.find("h1")
    if isinstance(header, Tag):
        return header.get_text(strip=True)

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find("main")
    if isinstance(main, Tag):
        paragraph = main.find("p")
        if isinstance(paragraph, Tag):
            return paragraph.get_text(strip= True)
    paragraph = soup.find("p")
    if isinstance(paragraph, Tag):
        return paragraph.get_text(strip=True)

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    urls: list[str] = []
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all("a")
    for i in a:
        if isinstance(i, Tag):
            href = i.get("href")
            if href is not None:
                abs_url = urljoin(base_url, href)  # pyright: ignore[reportArgumentType]
                urls.append(abs_url)
    return urls

def get_images_from_html(html:str, base_url:str) -> list[str]:
    images: list[str] = []
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find_all("img")
    for i in img:
        if isinstance(i, Tag):
            src = i.get("src")
            if src is not None:
                abs_path = urljoin(base_url, src)  # pyright: ignore[reportArgumentType]
                images.append(abs_path)
    return images

def extract_page_data(html: str, page_url:str) -> PageData:
    data_page = PageData(
        url=page_url,
        heading=get_heading_from_html(html),
        first_paragraph=get_first_paragraph_from_html(html),
        outgoing_links=get_urls_from_html(html, page_url),
        image_urls=get_images_from_html(html, page_url),
    )
    return data_page
