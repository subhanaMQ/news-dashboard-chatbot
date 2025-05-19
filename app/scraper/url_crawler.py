import requests
from bs4 import BeautifulSoup

def get_abc_urls():
    base_url = "https://www.abc.net.au/news"
    response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith("/news/") and href.count('-') > 3:
            full_url = "https://www.abc.net.au" + href
            links.add(full_url)
    return list(links)[:5]

def get_newscomau_urls():
    base_url = "https://www.news.com.au"
    response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if "/news-story/" in href:
            full_url = base_url + href if href.startswith("/") else href
            links.add(full_url)
    return list(links)[:5]

def get_all_article_urls():
    return get_abc_urls() + get_newscomau_urls()