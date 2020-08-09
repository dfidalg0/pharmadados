from requests import get
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def g1(q):
    html = get('https://g1.globo.com/busca/', {'q': q}).text

    html = BeautifulSoup(html, 'lxml')

    results = html.find(class_='results__list')

    if not results:
        return []

    L = []

    for result in results.find_all(class_='widget widget--card widget--info'):
        img = result.find('img')

        if img is not None:
            img = 'https:' + img.get('src')
        else:
            img = ''

        url = result.find('a')

        if url is None:
            continue

        url = 'https:' + url.get('href')

        title = result.find(class_='widget--info__title product-color')

        if title is None:
            continue

        title = title.text.strip()

        desc = result.find(class_='widget--info__description')

        if desc is None:
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
        r = list(pool.map(g1, query_list))
