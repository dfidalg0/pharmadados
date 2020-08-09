from requests import get
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def super_interessante(q):
    html = get('https://super.abril.com.br/', {
        's': q,
        'orderby': 'date'
    }).text

    html = BeautifulSoup(html, 'lxml')

    results = html.find(id='infinite-list')

    if not results:
        return []

    L = []

    for result in results.find_all(class_='card not-loaded list-item'):
        img = result.find('img')

        if img:
            img = img.get('src')
        else:
            img = ''

        url = result.find('a')

        if not url:
            continue

        url = url.get('href')

        title = result.find(class_='title')

        if not title:
            continue

        title = title.text.strip()

        desc = result.find(class_='description')

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
        r = list(pool.map(super_interessante, query_list))
