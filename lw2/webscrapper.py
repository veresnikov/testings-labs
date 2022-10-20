import datetime
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class URL:
    url: str
    previous_url: str
    status: int

    def __hash__(self):
        return url.__hash__()


result = set()
internal_urls = set()
invalid_urls = set()

total_urls_visited = 0

previous_url = ""


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_domain_name(url: str) -> str:
    return urlparse(url).netloc


def is_blocked_content_type(url: str) -> bool:
    types = {"mp4", "pdf", "doc", "docx", "xlsx", "xls", "ppt", "pptx", "jpeg", "jpg", "png", "rar", "7z", "zip",
             "webp", "webm", "gif"}
    for type in types:
        if url.find(type) != -1:
            return True


def find_all_links(url: str) -> set:
    global previous_url

    print('check ' + url)
    links = set()
    if is_blocked_content_type(url):
        req = requests.head(url, timeout=60)
        result.add(URL(url, previous_url, req.status_code))
        return links
    req = requests.get(url, timeout=60)
    result.add(URL(url, previous_url, req.status_code))
    soup = BeautifulSoup(req.content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue

        if urlparse(href).netloc == "":
            href = urljoin(url, href)

        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid_url(href):
            invalid_urls.add(href)
            continue
        if href in internal_urls:
            continue
        if get_domain_name(url) not in href:
            continue
        links.add(href)
        internal_urls.add(href)
        previous_url = url
    return links


def visit(url: str):
    global total_urls_visited
    total_urls_visited += 1
    links = find_all_links(url)
    for link in links:
        visit(link)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="simple web scrapper")
    parser.add_argument("url", help="testing url")

    args = parser.parse_args()
    url = args.url

    visit(url)

    with open(f"result/{get_domain_name(url)}_valid_internal_links.txt", "w") as f:
        total = 0
        print("Valid internal links".strip(), file=f)
        for link in result:
            if link.status < 400:
                print(link.url + " " + f"[{link.status}]".strip(), file=f)
                total += 1
        print(f"Check time: {datetime.datetime.now()}".strip(), file=f)
        print(f"Total links: {total}".strip(), file=f)

    with open(f"result/{get_domain_name(url)}_invalid_internal_links.txt", "w") as f:
        total = 0
        print("Invalid internal links".strip(), file=f)
        for link in result:
            if link.status > 400:
                print(link.previous_url + " -> " + link.url + " " + f"[{link.status}]".strip(), file=f)
                total += 1
        print(f"Check time: {datetime.datetime.now()}".strip(), file=f)
        print(f"Total links: {total}".strip(), file=f)
