#!/usr/bin/python3

from urllib.parse import urlparse
from crawler.error.urlerror import DomainUrlError
from crawler.utils.strtool import find_last_index

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

def patch(url, base_url):
    base_url_parse = urlparse(base_url)
    url_parse = urlparse(url)
    if base_url_parse.scheme == '' or base_url_parse.netloc == '':
        #case of baseUrl with error, raise it
        raise DomainUrlError("Base url can't parse domain url")
    if start_with(url, 'www'):
        #case of url without scheme, so I take it a default scheme 'http'
        return 'http://' + url
    elif start_with(url, '/'):
        #case of url with whole path, just need to add scheme and netloc
        return get_domain_url(base_url) + url
    elif not url_parse.scheme == '' and not url_parse.netloc == '':
        #case of url is ok, has all it need
        return url
    else:
        #case url without '/'
        path = base_url_parse.path
        if not path == '':
            #case of baseUrl with path and url without '/'
            path = path[0: find_last_index(path, '/')+1]
            return get_domain_url(base_url) + path + url
        else:
            #case of without '/' but in the root path
            return get_domain_url(base_url) + '/' + url


if __name__ == '__main__':
    url = 'index.html'
    base_url = 'http://www.dytt8.net'
    #print(url_patch(url, base_url))
    #base_url = 'http://www.dytt8.net/html/gndy/dyzz/index.html'
    #url =  'list_23_2.html'
    print(patch(url, base_url))
