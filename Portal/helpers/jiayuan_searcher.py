import urllib
import re
import http.cookiejar
import urllib.parse
import json

from urllib import request
from urllib.error import HTTPError
from collections import deque

# Create your models here.


class JiayuanSearcher:
    def __init__(self):
        self.host = 'http://search.jiayuan.com/v2/search_v2.php?key='
        self.record = set()
        self.queue = deque([])
        self.conditions = {'stc': {}}
        self.isLogin = False

    def login(self, account, password):
        cookie = http.cookiejar.CookieJar()  # 保存cookie，为登录后访问其它页面做准备
        cjhdr = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(cjhdr)
        urllib.request.install_opener(opener)

        url = "https://passport.jiayuan.com/dologin.php"
        data = urllib.parse.urlencode({'name': account, 'password': password, 'remem_pass': 'on', 'ljg_login': '1',
                                       'channel': '200', 'position': 204})
        data = data.encode('utf-8')
        res = urllib.request.urlopen(url, data)
        if res.status != 200:
            return ''
        return res.read().decode('utf-8')

    def get_params(self):
        params = ''
        for key in self.conditions:
            if key != 'stc':
                value = self.conditions[key]
            else:
                value = ''
                for index in self.conditions[key]:
                    value += '{0}:{1},'.format(index, self.conditions[key][index])
            params += '&{0}={1}'.format(key, value)
        return params

    def start(self):
        url = self.host + self.get_params()
        res = self.get_data_unicode(url)
        return res

    def get_data(self, url):
        data = request.urlopen(url).read()
        return data

    def get_data_unicode(self, url):
        data = self.get_data(url)
        return data.decode('utf-8')


class JiayuanHelper:
    def __init__(self, searcher):
        self.searcher = searcher
        region_dict = {11: '北京', 12: '天津', 13: '河北', 14: '山西', 15: '内蒙古', 21: '辽宁', 22: '吉林', 23: '黑龙江',
                       31: '上海', 32: '江苏', 33: '浙江', 34: '安徽', 35: '福建', 36: '江西', 37: '山东', 41: '河南',
                       42: '湖北', 43: '湖南', 44: '广东', 45: '广西', 46: '海南', 50: '重庆', 51: '四川', 52: '贵州',
                       53: '云南', 54: '西藏', 61: '陕西', 62: '甘肃', 63: '青海', 64: '宁夏', 65: '新疆', 71: '台湾',
                       81: '香港', 82: '澳门'}
        education_dict = {10: '中专', 20: '大专', 30: '本科', 50: '硕士', 60: '博士'}
        income_dict = {10: '2000以下', 20: '2000~5000元', 30: '5000~10000元', 40: '10000~20000元', 50: '20000元以上'}
        marriage_dict = {1: '未婚', 2: '离异', 3: '丧偶'}
        house_dict = {1: '未购房', 2: '已购房', 3: '与人合租', 4: '独自租房', 5: '与父母同住', 8: '需要时购置'}
        car_dict = {1: '暂未购车', 2: '已购车'}
        children_dict = {1: '无小孩', 2: '有小孩归自己', 3: '有小孩归对方'}
        job_dict = {1: '在校学生', 2: '计算机/互联网/IT', 3: '电子/半导体/仪表仪器', 4: '通信技术', 5: '销售', 6: '市场拓展',
                    7: '公关/商务', 8: '采购/贸易', 9: '客户服务/技术支持', 10: '人力资源/行政/后勤', 11: '高级管理',
                    12: '生产/加工/制造', 13: '质控/安检', 14: '工程机械', 15: '技工', 16: '财会/审计/统计', 17: '金融/证券/投资/保险',
                    18: '房地产/装修/物业', 19: '仓储/物流', 43: '交通/运输', 20: '普通劳动力/家政服务', 21: '普通服务行业',
                    22: '航空服务业', 23: '教育/培训', 24: '咨询/顾问', 25: '学术/科研', 26: '法律', 27: '设计/创意',
                    28: '文学/传媒/影视', 29: '餐饮/旅游', 30: '化工', 31: '能源/地质勘查', 32: '医疗/护理', 33: '保健/美容',
                    34: '生物/制药/医疗器械', 35: '体育工作者', 36: '翻译', 37: '公务员/国家干部', 38: '私营业主', 39: '农/林/牧/渔业',
                    40: '警察/其它', 41: '自由职业者', 42: '其他'}
        blood_dict = {1: 'A', 2: 'B', 3: 'O', 4: 'AB', 5: '其他'}
        self.sex_dict = {'m': '男', 'f': '女'}
        self.stc_type_dict = {1: 'select_one', 2: 'range', 3: 'range', 4: 'select_above', 5: 'select_above',
                              6: 'select_one', 7: 'select_one', 8: 'select_one', 13: 'select_one', 14: 'select_one',
                              18: 'select_one'}
        self.stc_name_dict = {1: '地区', 2: '年龄', 3: '身高', 4: '教育', 5: '收入', 6: '婚姻', 7: '购房', 8: '购车',
                              13: '子女', 14: '工作', 18: '血型'}
        self.stc_value_dict = {1: region_dict, 2: range(18, 61), 3: range(150, 190), 4: education_dict, 5: income_dict,
                               6: marriage_dict, 7: house_dict, 8: car_dict, 13: children_dict, 14: job_dict,
                               18: blood_dict}

    def set_sex(self, sex=''):
        self.searcher.conditions['sex'] = sex

    def set_value(self, index, value1, value2=None):
        if value1 == 0 and index in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][index]
            return False

        if not value2:
            value2 = 0

        if self.stc_type_dict == 'select_one':
            self.searcher.conditions['stc'][index] = value1
        else:
            res = '{0}.{1}'.format(value1, value2)
            self.searcher.conditions['stc'][index] = res

    def start_single(self, row):
        res = self.searcher.start()
        return self.process_single(self.get_data_of_json(res), row)

    def get_data_of_json(self, string):
        idxl = string.find('{')
        idxr = string.rfind('}')
        string = string[idxl: idxr + 1]
        obj = json.loads(string)
        return obj['userInfo']

    def process_single(self, user_list, index):
        attr_dict = {2: 'age', 3: 'height', 4: 'education', 6: 'marriage'}
        count_dict = {}
        if not index in attr_dict:
            return
        attr_name = attr_dict[index]
        for user in user_list:
            val = user[attr_name]
            if not val in count_dict:
                count_dict[val] = 1
            else:
                count_dict[val] += 1
        return count_dict

    def generate_data(self, count_dict):
        tempSet = set()
        labels = []
        data = []
        for key in count_dict:
            tempSet.add(key)
        for key in tempSet:
            labels.append(key)
            data.append(count_dict[key])
        datasets = [{'label': 'Dataset',
                     'fillColor': 'rgba(220,220,220,0.5)',
                     'strokeColor': "rgba(220,220,220,0.8)",
                     'highlightFill': "rgba(220,220,220,0.75)",
                     'highlightStroke': "rgba(220,220,220,1)",
                     'data': data}]
        return {'labels': labels, 'datasets': datasets}
