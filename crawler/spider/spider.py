#!/usr/bin/python3

import requests
import re

from collections import deque
from crawler.utils import urltool
from crawler.analyse import moviefilter

def spider(init_urls, black_list, encode_dict):
    queue = deque(init_urls)
    visited = set(black_list)
    cnt = 0

    while queue:
        url = queue.popleft()
        visited |= {url}

        print('has catch:', cnt, 'now catching -->', url)
        urlres = requests.get(url)
        if 'html' not in urlres.headers['Content-Type']:
            continue

        cnt += 1
        urltool.encode_change(urlres, encode_dict)
        
        list_re = re.compile('/gndy/dyzz')
        movie_re = re.compile('/gndy/dyzz/[0-9]+/[0-9]+')
        
        #print(list_re.search(url))

        if not list_re.search(url) == None:
            if movie_re.search(url) == None:
                html_collect(urlres, queue, visited, black_list)
            else:
                moviefilter.html_analyse(urlres.text)


def html_collect(response, queue, visited, black_list):
    href_re = re.compile('href=[\'|\"](.+?)[\'|\"]')
    url_re = re.compile('url=(.+?)[\'|\"]')

    text = response.text
    base_url = response.url

    for url in url_re.findall(text):
        url = urltool.url_patch(url, base_url)
        if url not in visited and not urltool.black_list_check(url, black_list):
            queue.append(url)
            print('get redirect url:', url)
            return

    for url in href_re.findall(text):
        url = urltool.url_patch(url, base_url)
        if url not in visited and not urltool.black_list_check(url, black_list):
            queue.append(url)
            print('get url:', url)

if __name__ == '__main__':
    init_urls = ['http://www.dytt8.net/html/gndy/dyzz/index.html']
    black_list = ['http://www.ygdy8.net']
    encode_dict = {'http://www.dytt8.net': 'gb2312'}
    spider(init_urls, black_list, encode_dict)
