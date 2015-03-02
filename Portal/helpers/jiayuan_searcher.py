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
        self.region_dict = {}
        self.marriage_dict = {1: '未婚', 2: '离异', 3: '丧偶'}
        self.education_dict = {10: '中专', '': '大专', '': '本科', '': '硕士', '': '博士'}
        self.income_dict = {}
        self.house_dict = {}
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

    def set_education(self, education='', above=0):
        if education == '' and 4 in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc'][4]
            return
        height = '{0}.{1}'.format(education, above)
        self.searcher.conditions['stc'][3] = height


    def set_marriage(self, marriage=''):
        if marriage == '' and '6' in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc']['6']
            return
        self.searcher.conditions['stc']['6'] = marriage

    def set_photo(self, tof=False):
        if not tof and '23' in self.searcher.conditions['stc']:
            del self.searcher.conditions['stc']['23']
            return
        self.searcher.conditions['stc']['23'] = '1'

