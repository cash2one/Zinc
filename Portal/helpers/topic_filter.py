from urllib import request


def get_data(url):
    data = request.urlopen(url).read()
    return data.decode('UTF-8')


class BaiduFilter:
    url = ''
    datas = []

    def __init__(self, url):
        self.url = url + '?see_lz=1'


    def start(self):
        pass