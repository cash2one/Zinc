import re
from django.test import TestCase
from Portal.helpers.loop_requester import LoopSpider
from Portal.helpers.topic_filter import BaiduFilter, TianyaFilter
from Portal.helpers.jiayuan_searcher import JiayuanSearcher, JiayuanHelper


class LoopSpiderTestCase(TestCase):
    def setUp(self):
        self.spider = LoopSpider('')

    def test_get_host_of_url(self):
        url1 = 'http://www.baidu.com'
        url2 = 'http://www.baidu.com/'
        url3 = 'https://www.baidu.com'
        url4 = 'https://www.baidu.com/'
        url5 = 'http://www.baidu.com/index'
        url6 = 'http://www.baidu.com/index.html'
        self.assertEqual(self.spider.get_host(url1), url1)
        self.assertEqual(self.spider.get_host(url2), url1)
        self.assertEqual(self.spider.get_host(url3), url3)
        self.assertEqual(self.spider.get_host(url4), url3)
        self.assertEqual(self.spider.get_host(url5), url1)
        self.assertEqual(self.spider.get_host(url6), url1)

    def test_get_domain_of_url(self):
        url0 = 'www.baidu.com'
        url1 = 'http://www.baidu.com'
        url2 = 'https://www.baidu.com'
        self.assertEqual(self.spider.get_domain(url1), url0)
        self.assertEqual(self.spider.get_domain(url2), url0)

    def test_get_parent_of_url(self):
        url1 = 'http://www.baidu.com'
        url2 = 'http://www.baidu.com/index'
        url3 = 'http://www.baidu.com/index/'
        url4 = 'http://www.baidu.com/index.html'
        url5 = 'http://www.baidu.com/index.html/'
        url6 = 'http://www.baidu.com/index/index.html'
        url7 = 'http://www.baidu.com/index/index.html/'
        self.assertEqual(self.spider.get_parent(url2), url1)
        self.assertEqual(self.spider.get_parent(url3), url1)
        self.assertEqual(self.spider.get_parent(url4), url1)
        self.assertEqual(self.spider.get_parent(url5), url1)
        self.assertEqual(self.spider.get_parent(url6), url2)
        self.assertEqual(self.spider.get_parent(url7), url2)

    def test_full_url_of_url(self):
        url1 = 'http://www.baidu.com'
        url2 = 'http://www.baidu.com/index'
        url3 = 'http://www.baidu.com/index.html'
        url4 = 'http://www.baidu.com/index/index.html'
        rel1 = 'test.html'
        rel2 = '/test.html'
        self.assertEqual(self.spider.get_full_url(url1), url1)
        self.assertEqual(self.spider.get_full_url(url2), url2)
        self.assertEqual(self.spider.get_full_url(rel1, url3), 'http://www.baidu.com/test.html')
        self.assertEqual(self.spider.get_full_url(rel2, url3), 'http://www.baidu.com/test.html')
        self.assertEqual(self.spider.get_full_url(rel1, url4), 'http://www.baidu.com/index/test.html')
        self.assertEqual(self.spider.get_full_url(rel2, url4), 'http://www.baidu.com/test.html')

    def test_get_data_of_url_success(self):
        url = 'https://raw.githubusercontent.com/trotyl/Static/master/fake_data'
        data, sth = self.spider.get_data(url)
        data = data.decode('UTF-8')
        self.assertEqual(data, 'ABCD\n')

    def test_get_data_of_url_fail(self):
        url = 'https://raw.githubusercontent.com/trotyl/Static/master/not_exist'
        data, sth = self.spider.get_data(url)
        self.assertFalse(data)

    def test_get_list_of_url_many(self):
        url = 'https://raw.githubusercontent.com/trotyl/Static/master/fake_baidu.html'
        data, sth = self.spider.get_data(url)
        url_list = self.spider.get_list(data)
        self.assertEqual(len(url_list), 126)

    def test_get_list_of_url_zero(self):
        url = 'https://raw.githubusercontent.com/trotyl/Static/master/empty.html'
        data, sth = self.spider.get_data(url)
        url_list = self.spider.get_list(data)
        self.assertEqual(url_list, [])

    def test_loop_state(self):
        spider = LoopSpider('https://raw.githubusercontent.com/trotyl/Static/master/index.html')
        record = spider.start()
        self.assertEqual(len(record), 5)


class BaiduFilterTestCase(TestCase):
    def setUp(self):
        pass

    def test_filter_state(self):
        baidu = BaiduFilter('3506527161')
        title, topics = baidu.start()
        self.assertEqual(title, '深夜失眠说说我的初恋')
        self.assertGreaterEqual(len(topics), 53)


class TianyaFilterTestCase(TestCase):
    def setUp(self):
        pass

    def test_filter_state(self):
        tianya = TianyaFilter('http://bbs.tianya.cn/post-394-129735-1.shtml')
        title, topics = tianya.start()
        self.assertEqual(title, '异地恋的姐妹们，进来聊聊我们苦逼的生活。')
        self.assertGreaterEqual(len(topics), 62)


class JiayuanSearcherTestCase(TestCase):
    def setUp(self):
        pass

    def test_login(self):
        jiayuan = JiayuanSearcher()
        res = jiayuan.login('yzj1995@vip.qq.com', '16777216')
        match = re.search('top\.location\.href', res)
        self.assertTrue(match)

    def test_searcher_state(self):
        jiayuan = JiayuanSearcher()
        jiayuan.login('yzj1995@vip.qq.com', '16777216')
        jiayuan.conditions['sex'] = 'f'
        res = jiayuan.start()
        match = re.search('"isLogin":true', res)
        self.assertTrue(match)


class JiayuanHelperTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_data_of_json(self):
        json_string = '##jiayser##{"isLogin":true,"count":30254,"pageTotal":1211,"userInfo":' \
                      '[{"uid":132917123,"realUid":133917123,"nickname":"","sex":"","sexValue":"f",' \
                      '"randAttr":"formal","marriage":"","height":"160","education":"","income":null,' \
                      '"work_location":"","work_sublocation":"","age":18,"image":"","count":"30254","online":0,' \
                      '"randTag":"","randListTag":"","userIcon":"","helloUrl":"","sendMsgUrl":"","shortnote":"",' \
                      '"matchCondition":""},' \
                      '{"uid":132825533,"realUid":133825533,"nickname":"","sex":"","sexValue":"f",' \
                      '"randAttr":"formal","marriage":"","height":"165","education":"","income":null,' \
                      '"work_location":"","work_sublocation":"","age":18,"image":"","count":"30254","online":1,' \
                      '"randTag":"","randListTag":"","userIcon":"","helloUrl":"","sendMsgUrl":"","shortnote":"",' \
                      '"matchCondition":""}],' \
                      '"condi":{"age":{"min":"18","max":"20"},"nation":["1"]}}##jiayser##//'
        jiayuan = JiayuanSearcher()
        helper = JiayuanHelper(jiayuan)
        res = helper.get_data_of_json(json_string)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['uid'], 132917123)
