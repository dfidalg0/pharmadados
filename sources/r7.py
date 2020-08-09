from requests import get
from json import loads
from concurrent.futures import ThreadPoolExecutor


def r7(q):
    json = get('https://cse.google.com/cse/element/v1', {
        'rsz': 'filtered_cse',
        'num': 20,
        'hl': 'pt-PT',
        'source': 'gcsc',
        'gss': '.com',
        'cselibv': '26b8d00a7c7a0812',
        'cx': '004434994716415441538:jtto9b0nerq',
        'q': q,
        'safe': 'off',
        'cse_tok': 'AJvRUv2woFsRFhY5E_v2yIDi6eMN:1596845049424',
        'filter': 1,
        'sort': '',
        'exp': 'csqr,  cc',
        'callback': 'google.search.cse.api'
    }).text

    json = loads(json[json.find('{'):-2])

    results = json['results']

    L = []

    for result in results:
        url = result['url']

        if 'noticias.r7' not in url:
            continue

        title = result['titleNoFormatting']
        desc = result['contentNoFormatting']

        idx = desc.find('...')
        if idx != -1:
            contents = desc.split('...')
            desc = contents[1].strip()
            if len(contents) > 2:
                desc += ' ...'

        try:
            img = result['richSnippet']['cseImage']['src']
        except KeyError:
            img = ''

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
        r = list(pool.map(r7, query_list))
