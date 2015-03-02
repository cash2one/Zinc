import urllib
import re

from urllib import request
from urllib.error import HTTPError
from collections import deque


# Create your models here.


class JiayuanSearcher:

    def __init__(self):
        self.host = 'http://search.jiayuan.com/v2/index.php?key='
        self.record = set()
        self.queue = deque([])
        self.conditions = {'stc': {}}

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
        pass


class JiayuanHelper:

    def __init__(self, searcher):
        self.searcher = searcher
        self.sex_dict = {'m': '男', 'f': '女'}
        self.region_dict = {11: '北京', 12: '天津', 13: '河北', 14: '山西', 15: '内蒙古', 21: '辽宁', 22: '吉林', 23: '黑龙江',
                            31: '上海', 32: '江苏', 33: '浙江', 34: '安徽', 35: '福建', 36: '江西', 37: '山东', 41: '河南',
                            42: '湖北', 43: '湖南', 44: '广东', 45: '广西', 46: '海南', 50: '重庆', 51: '四川', 52: '贵州',
                            53: '云南', 54: '西藏', 61: '陕西', 62: '甘肃', 63: '青海', 64: '宁夏', 65: '新疆', 71: '台湾',
                            81: '香港', 82: '澳门'}
        self.marriage_dict = {1: '未婚', 2: '离异', 3: '丧偶'}
        self.education_dict = {10: '中专', 20: '大专', 30: '本科', 50: '硕士', 60: '博士'}
        self.income_dict = {10: '2000以下', 20: '2000~5000元', 30: '5000~10000元', 40: '10000~20000元', 50: '20000元以上'}
        self.house_dict = {1: '未购房', 2: '已购房', 3: '与人合租', 4: '独自租房', 5: '与父母同住', 8: '需要时购置'}
        self.car_dict = {}
        self.children_dict = {}
        self.job_dict = {}
        self.company_dict = {}
        self.nation_dict = {}
        self.blood_dict = {}
        self.animal_dict = {}
        self.constellation_dict = {}

    def set_sex(self, sex):
        self.searcher.conditions['sex'] = sex

    def set_region(self, region=''):
        if region == '' and 1 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][1]
            return
        self.searcher.conditions['stc']['1'] = region

    def set_age(self, start=0, end=0):
        if start == 0 and 2 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][2]
            return
        age = '{0}.{1}'.format(start, end)
        self.searcher.conditions['stc'][2] = age

    def set_height(self, start=0, end=0):
        if start == 0 and 3 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][3]
            return
        height = '{0}.{1}'.format(start, end)
        self.searcher.conditions['stc'][3] = height

    def set_education(self, education=0, above=0):
        if education == 0 and 4 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][4]
            return
        height = '{0}.{1}'.format(education, above)
        self.searcher.conditions['stc'][4] = height

    def set_income(self, income=0, above=0):
        if income == 0 and 5 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][5]
            return
        height = '{0}.{1}'.format(income, above)
        self.searcher.conditions['stc'][5] = height

    def set_marriage(self, marriage=0):
        if marriage == 0 and 6 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][6]
            return
        self.searcher.conditions['stc'][6] = marriage

    def set_house(self, house=0):
        if house == 0 and 7 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][7]
            return
        self.searcher.conditions['stc'][7] = house


    def set_photo(self, tof=0):
        if tof == 0 and 23 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][23]
            return
        self.searcher.conditions['stc'][23] = '1'

