from urllib.request import urlopen
from urllib.error import URLError
from io import TextIOWrapper
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def get_all_urls_from_page_content(soup: BeautifulSoup) -> set:
    urls = set()
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url[0] == '/' and url != '/':
            url = base_url + url
        if url.startswith(base_url) and url not in urls:
            urls.add(url)
    return urls


def process_text(soup: BeautifulSoup, search_query: str):
    text_list = soup.get_text('#').split('#')
    found_occurrences = []
    search_query = search_query.lower()
    for text in text_list:
        if search_query in text.lower():
            found_occurrences.append(text)
    return found_occurrences



def get_all_urls(base_url: str, search_query: str) -> set:
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
        urls_to_visit = urls_to_visit.union(get_all_urls_from_page_content(soup))
        text_found = process_text(soup, search_query)
    return visited_urls


base_url = "https://yandex.cloud"
search_query = "бизнес"
all_page_urls = get_all_urls(base_url, search_query)
