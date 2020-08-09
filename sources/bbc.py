from concurrent.futures import ThreadPoolExecutor


def bbc(q):
    from requests import get
    from bs4 import BeautifulSoup

    html = get('https://www.bbc.com/portuguese/search', {
        'q': q
    }).text

    html = BeautifulSoup(html, 'lxml')

    results = html.find(class_='ws-search-components')

    if not results:
        return []

    L = []

    for result in results.find_all(class_='hard-news-unit hard-news-unit--regular faux-block-link'):
        img = ''

        url = result.find('a')

        if not url:
            continue

        url = url.get('href')

        title = result.find(class_='hard-news-unit__headline')

        if not title:
            continue

        title = title.text.strip()

        desc = result.find(class_='hard-news-unit__summary')

        if not desc:
            continue

        desc = desc.text.strip()

        L.append({
            'title': title,
            'description': desc,
            'img_src': img,
            'url': url
        })

    return L


if __name__ == '__main__':
    query_list = ['cloroquina', 'ivermectina', 'ozonio', 'dexametasona']

    with ThreadPoolExecutor(max_workers=10) as pool:
        r = list(pool.map(bbc, query_list))
