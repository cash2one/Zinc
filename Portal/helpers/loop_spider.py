from urllib import request
from collections import deque
import re

# Create your models here.


class LoopSpider:
    domain = ''
    record = {}
    queue = deque([])

    def __init__(self, domain):
        domain = domain.trim()
        self.domain = domain
        self.queue.append(domain)
        self.record[domain] = False
        self.start()

    def start(self):
        if self.domain == '':
            return
        counter = 0
        while len(self.queue) != 0 and counter < 100000:
            current = self.queue.popleft()
            self.record[current] = True
            data = self.get_data(current)
            self.save_data(data, current)
            url_list = self.get_list(data)
            self.append_queue(url_list)

    def get_data(self, url):
        data = request.urlopen(url).read()
        return data

    def get_list(self, data):
        data = data.decode('UTF-8')
        url_list = re.findall('href\W?=\W?[\'\"].*?[\'\"]', data)
        return url_list

    def append_queue(self, url_list):
        for link in url_list:
            self.queue.append(link)

    def save_data(self, url, data):
        rel = url.replace(self.domain, '')
        if rel.endswith('/'):
            rel = rel[:-1]
        if len(rel) == 0:
            rel = 'index'
        if rel.find('.') == -1:
            rel += '.html'
        file = open(self.domain + '\\' + rel, 'w+')
        file.write(data)
        file.close()


