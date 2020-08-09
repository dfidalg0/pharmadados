from requests import get
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def estadao(q):
    html = get('https://busca.estadao.com.br/', {'q': q, 'tipo_conteudo': 'Notícias', 'editoria[]': 'Saúde'}).text

    html = BeautifulSoup(html, 'lxml')

    results = html.find(class_='col-md-8 col-sm-12 col-xs-12 content')

    L = []

    for result in results.find_all(class_='col-md-12 col-sm-12 col-xs-12 init item-lista item-lista-busca'):
        img = result.find('img')

        if img:
            img = img.get('data-src-desktop')
        else:
            img = ''

        url = result.find(class_='link-title')

        if url is None:
            continue

        url = url.get('href')

        title = result.find('h3')

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
        r = list(pool.map(estadao, query_list))
