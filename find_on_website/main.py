from urllib.request import urlopen
from urllib.error import URLError
from io import TextIOWrapper
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def get_all_urls(base_url: str) -> set:
    visited_urls = set()
    urls_to_visit = {base_url}

    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop()
        if current_url not in visited_urls:
            print(f'Crawling: {current_url}')
            try:
                with urlopen(current_url) as response:
                    content = TextIOWrapper(response, encoding='utf-8').read()
            except URLError as e:
                print(e.reason)
                continue
        visited_urls.add(current_url)
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            url = link['href']
            if url[0] == '/' and url != '/':
                url = base_url + url
            if url.startswith(base_url) and url not in visited_urls:
                urls_to_visit.add(url)

    return visited_urls


base_url = "https://yandex.cloud"
all_page_urls = get_all_urls(base_url)
