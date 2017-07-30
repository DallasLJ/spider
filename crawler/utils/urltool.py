#!/usr/bin/python3

from urllib.parse import urlparse
from crawler.error.urlerror import DomainUrlError

def start_with(str, prefix):
    if str[0: len(prefix)] == prefix:
        return True
    else:
        return False

def get_domain_url(url):
    url_parse = urlparse(url)
    if not url_parse.scheme == '' and not url_parse.netloc == '':
        return url_parse.scheme + '://' + url_parse.netloc
    else:
        raise DomainUrlError("Base url can't parse domain url")

def url_patch(url, base_url):
    if start_with(url, 'www'):
        return 'http://' + url
    if not start_with(url, '/') and not start_with(url, 'http') and not start_with(url, 'ftp'):
        url = '/' + url
    if urlparse(url).netloc == '':
        try:
            return get_domain_url(base_url) + url
        except DomainUrlError as e:
            print(e.message)
    else:
        return url

def dytt_patch(url, base_url):
    if start_with(url, 'list'):
        base_url = base_url[::-1]
        base_url = base_url[base_url.find('/'):]
        base_url = base_url[::-1]
        return base_url + url
    else:
        return url_patch(url, base_url)

def encode_change(response, encode_dict):
    url = response.url
    for key in encode_dict.keys():
        if start_with(url, key):
            response.encoding = encode_dict[key]
            return

def black_list_check(url, black_list):
    domain_url = get_domain_url(url)
    if domain_url in black_list:
        return True
    return False

if __name__ == '__main__':
    url = 'index.html'
    base_url = 'http://www.dytt8.net'
    #print(url_patch(url, base_url))
    #base_url = 'http://www.dytt8.net/html/gndy/dyzz/index.html'
    #url =  'list_23_2.html'
    print(dytt_patch(url, base_url))
