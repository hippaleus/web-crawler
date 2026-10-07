# Web Crawler

An async Python CLI that crawls a website and generates a JSON report of every
internal page it finds — URL, heading, and extracted data — with each page
visited exactly once.

Built as part of Boot.dev's Python web crawler project, with
asyncio concurrency, rate limiting, a visit lock to prevent duplicate crawls,
CLI-configurable crawl limits, and JSON report output.

## Features

- Recursive crawl restricted to the base domain (external links skipped)
- Concurrent fetching via `aiohttp` + `asyncio`, capped by a semaphore
- With `asyncio.Lock` — no page is crawled twice
- Optional page limit as a safety valve
- Per-page extraction with BeautifulSoup (heading, links, images)
- JSON report of the full crawl (see `sample_report.json` for output shape)
- Unit-tested core (`normalize_url`, HTML parsing, link/image extraction)

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Usage

    uv run main.py &lt;url&gt; [max_pages] [max_concurrency]

Examples:

    # full crawl of a site, default concurrency
    uv run main.py https://example.com

    # stop after 50 pages
    uv run main.py https://example.com 50

    # stop after 50 pages, up to 5 concurrent requests
    uv run main.py https://example.com 50 5

The crawl writes its findings as JSON — one entry per page crawled.

## Sample output

See [`sample_report.json`](./sample_report.json) for the full output shape
(from a crawl of a practice ecommerce site).

## Running tests

    uv run -m unittest

## Project structure

    main.py          – CLI entry point and AsyncCrawler class (async crawl engine)
    crawl.py         – URL normalization and HTML extraction (pure functions, tested)
    json_report.py   – writes the crawl results to JSON
    sample_report.json – example crawler output (sample, not regenerated)

## Notes

- Crawls are rate-limited and same-domain by design. Point it only at sites
  you have permission to crawl.
