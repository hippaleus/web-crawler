from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Tag


def normalize_url(url:str) -> str | None:
    split = urlsplit(url)
    # first = split._replace(netloc="boot.dev").geturl()
    # second: str = split._replace(scheme="http").geturl()
    # third: str = split._replace(fragment="").geturl()
    # fourth: str = split._replace(path="pricing").geturl()
    # fifth: str = split._replace(scheme="").geturl()
    return f"{split.netloc}{split.path}"

def get_heading_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, 'html.parser')
    header = soup.find("h1")
    if isinstance(header, Tag):
        print(f'The header found contains: "{header.get_text(strip=True)}" in unicode string.')
        return header.get_text(strip=True)

def get_first_paragraph_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find("main")
    if isinstance(main, Tag):
        paragraph = main.find("p")
        print(f"main tag is found.")
        if isinstance(paragraph, Tag):
            print(f'The paragraph found inside of main contains the following:\n"{paragraph.get_text(strip=True)}"')
            return paragraph.get_text(strip= True)
    paragraph = soup.find("p")
    if isinstance(paragraph, Tag):
        print(f'The following paragraph was not found outside of main:\n"{paragraph.get_text(strip=True)}"')
        return paragraph.get_text(strip=True)

def get_urls_from_html(html: str, base_url: str) -> list[str]| None:
    urls: list = []
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all("a")
    print(a)
    for i in a:
        if isinstance(i, Tag):
            print(i.get("href"))
            # urls = i.get("href")
            urls.append(i.get("href"))
            return urls

def get_images_from_html(html:str):
    pass
