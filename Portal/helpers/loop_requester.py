import urllib
import re

from urllib import request, parse
from urllib.error import HTTPError
from collections import deque


# Create your models here.


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip('\\')
    exists = os.path.exists(path)

    if not exists:
        os.makedirs(path)
        return True
    else:
        return False


def get_host(url):
    match = re.match('http[s]?://([^/"\']+)', url)
    if match:
        return match.group(0)
    return ''


def get_domain(url):
    host = get_host(url)
    idx = host.find('://')
    return host[idx + 3:]


def get_parent(url):
    url = url.rstrip('/')
    idx = url.rfind('/')
    return url[:idx]


def get_full_url(url, current=''):
    if url.startswith('http'):
        return url
    if url == '/':
        return get_host(current)
    if url.startswith('//'):
        return 'http:' + url
    if url.startswith('/'):
        return get_host(current) + url
    else:
        return get_parent(current) + '/' + url


def get_data(url):
    try:
        res = request.urlopen(url)
        data = res.read()
        full_url = res.geturl()
    except HTTPError:
        data = False
        full_url = ''
    return data, full_url


def get_list(data):
    try:
        data = data.decode('UTF-8')
        url_list = re.findall('(?:href|src)=\"([^\'\"]+)\"', data)
        return list(set(url_list))
    except UnicodeDecodeError:
        return []


def save_data(data, url):
    if not url.startswith('http'):
        return
    if url.startswith('#'):
        return
    if url.endswith('/'):
        url += 'index.html'
    elif url == get_host(url):
        url += '/index.html'
    elif url.rfind('.') < url.rfind('/'):
        url += '.html'
    idxl = url.find('://')
    idxr = url.rfind('/')
    path = url[idxl + 3: idxr]
    mkdir('download/' + path)
    file = open('download/' + url[idxl + 3:], 'wb')
    file.write(data)
    file.close()


class LoopSpider:

    def __init__(self, start_page):
        if not start_page.startswith('http'):
            start_page = 'http://' + start_page
        host = get_host(start_page)
        if host == '':
            return
        self.host = host
        self.record = set()
        self.queue = deque([])
        self.queue.append(start_page)

    def start(self):
        if self.host == '':
            return set()
        while len(self.queue) != 0 and len(self.record) < 20:
            current = self.queue.popleft()
            data, url = get_data(current)
            if not data or url in self.record:
                continue
            self.record.add(url)
            save_data(data, url)
            url_list = get_list(data)
            self.append_queue(url_list, current)
        return self.record

    def append_queue(self, url_list, current):
        for link in url_list:
            url = get_full_url(link, current)
            if not get_host(url) == self.host:
                continue
            if not url in self.record:
                self.queue.append(url)

