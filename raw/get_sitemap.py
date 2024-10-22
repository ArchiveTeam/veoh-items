import gzip
import os
import re
import typing

import requests


def get_url(url: str) -> bytes:
    print(url)
    response = requests.get(url)
    print(response)
    if response.status_code == 404:
        return b''
    assert response.status_code == 200
    if not os.path.isdir('sitemap'):
        os.makedirs('sitemap')
    with open(os.path.join('sitemap', url.rsplit('/', 1)[1]), 'wb') as f:
        content = response.content
        f.write(content)
        return content


def sitemap_items() -> typing.Iterator[str]:
    response = get_url('https://scache.veoh.com/sitemap/sitemap.xml')
    for url in re.findall(r'<loc>\s*([^\s<]+)', str(response, 'utf8')):
        sitemap = str(gzip.decompress(get_url(url)), 'utf8')
        i = 0
        for i, identifier in enumerate(re.findall(r'veoh\.com/watch/([0-9a-zA-Z]+)', sitemap)):
            yield 'video:' + identifier
        print(i)


def main():
    with open('video_sitemap.txt', 'w') as f:
        for line in sitemap_items():
            f.write(line+'\n')

if __name__ == '__main__':
    main()

