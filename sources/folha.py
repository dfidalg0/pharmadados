from requests import get
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def folha(q):
    html = get('https://search.folha.uol.com.br/search', {'q': q, 'site': 'jornal'}).text

    html = BeautifulSoup(html, 'lxml')

    results = html.find(class_='u-list-unstyled c-search')

    L = []

    for result in results.find_all(class_='c-headline c-headline--newslist'):
        categoria = result.find('h3').text

        if 'Opinião' in categoria:
            continue

        img = result.find('img')

        if img:
            img = img.get('src')
        else:
            img = ''

        url = result.find('a')

        if url is None:
            continue

        url = url.get('href')

        title = result.find('h2')

        if title is None:
            continue

        title = title.text.strip()

        desc = result.find('p')

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
        r = list(pool.map(folha, query_list))
