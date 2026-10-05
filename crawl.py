from urllib.parse import urlsplit


def normalize_url(url:str) -> str | None:
    split = urlsplit(url)
    # first = split._replace(netloc="boot.dev").geturl()
    # second: str = split._replace(scheme="http").geturl()
    # third: str = split._replace(fragment="").geturl()
    # fourth: str = split._replace(path="pricing").geturl()
    # fifth: str = split._replace(scheme="").geturl()
    return f"{split.netloc}{split.path}"
