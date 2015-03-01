import re

from urllib import request


class BaiduFilter:

    def __init__(self, url):
        if url == '':
            return
        if url.isdigit():
            url = 'http://tieba.baidu.com/p/' + url
        if not url.startswith('http'):
            url = 'http://' + url
        self.url = url + '?see_lz=1'
        self.count = 0
        self.title = ''
        self.data = []

    def start(self):
        page = self.get_data_unicode(self.url)
        self.get_count(page)
        self.get_title(page)

        for i in range(1, self.count + 1):
            paras = self.get_page(i)
            for para in paras:
                self.data.append(para)
        return self.title, self.data

    def get_count(self, page):
        match = re.search(r'class="red">(\d+?)</span>', page)
        if match:
            count = int(match.group(1))
        else:
            count = 0
        self.count = count

    def get_title(self, page):
        match = re.search(r'<h1.*?>(.*?)</h1>', page)
        if match:
            title = match.group(1)
        else:
            title = '暂无标题'
        self.title = title

    def get_page(self, number):
        url = self.url + '&pn=' + str(number)
        page = self.get_data_unicode(url)
        return self.filter_data(page)

    def filter_data(self, page):
        items = re.findall('id="post_content.*?>(.*?)</div>', page)
        return items

    def get_data(self, url):
        data = request.urlopen(url).read()
        return data

    def get_data_unicode(self, url):
        data = self.get_data(url)
        return data.decode('utf-8')


class TianyaFilter:

    def __init__(self, url):
        if url == '':
            return
        if url.isdigit():
            url = 'http://bbs.tianya.cn/post-funinfo-' + url
        if not url.startswith('http'):
            url = 'http://' + url
        idx1 = url.rfind('-')
        self.url = url[:idx1]
        self.count = 0
        self.title = ''
        self.data = []

    def start(self):
        page = self.get_data_unicode(self.url + '-1.shtml')
        self.get_count(page)
        self.get_title(page)
        self.data.append(self.get_topic(page))
        for i in range(1, self.count + 1):
            paras = self.get_page(i)
            for para in paras:
                self.data.append(para)
        return self.title, self.data

    def get_count(self, page):
        match = re.search(r'<a.*?>(\d+?)</a>\W+?<a.*?>下页</a>', page)
        if match:
            count = int(match.group(1))
        else:
            count = 0
        self.count = count

    def get_title(self, page):
        match = re.search(r'<span style="font-weight:400;">(.*?)</span>', page)
        if match:
            title = match.group(1)
        else:
            title = '暂无标题'
        self.title = title

    def get_topic(self, page):
        match = re.search(r'<div class="bbs-content clearfix">\s+(.*?)\s+</div>', page)
        if match:
            topic = match.group(1)
        else:
            topic = '未发现主题'
        return topic

    def get_page(self, number):
        url = self.url + '-' + str(number) + '.shtml'
        page = self.get_data_unicode(url)
        return self.filter_data(page)

    def filter_data(self, page):
        items = re.findall('<span><strong class="host">楼主.*?<div class="bbs-content">(.*?)</div>', page, re.S)
        return items

    def get_data(self, url):
        data = request.urlopen(url).read()
        return data

    def get_data_unicode(self, url):
        data = self.get_data(url)
        return data.decode('utf-8')
