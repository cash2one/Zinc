import json
from django.shortcuts import render
from Portal.helpers.loop_requester import LoopSpider
from Portal.helpers.topic_filter import BaiduFilter, TianyaFilter
from Portal.helpers.jiayuan_searcher import JiayuanSearcher, JiayuanHelper
from Portal.helpers.zip_dir import zip_dir
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'Portal/index.html')


def loop(request):
    if request.method == 'GET':
        return render(request, 'Portal/loop_spider.html')
    elif request.method == 'POST':
        address = request.POST['address']
        spider = LoopSpider(address)
        record = spider.start()
        return render(request, 'Portal/loop_spider.html', {'address': address, 'result_list': record})


def loop_zip(request):
    address = request.GET['address']
    dir_name = 'download/' + address
    file_name = 'zip/' + address + '.zip'
    zip_dir(dir_name, file_name)
    file = open(file_name, 'rb').read()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=' + address + '.zip'
    response.write(file)
    return response


def baidu(request):
    if request.method == 'GET':
        return render(request, 'Portal/topic_filter.html', {'type': '百度贴吧', 'holder': 'tieba.baidu.com/p/3506527161'})
    elif request.method == 'POST':
        address = request.POST['address']
        baidu_filter = BaiduFilter(address)
        title, topics = baidu_filter.start()
        return render(request, 'Portal/topic_filter.html',
                      {'type': '百度贴吧', 'address': address, 'title': title, 'result_list': topics})


def tianya(request):
    if request.method == 'GET':
        return render(request, 'Portal/topic_filter.html',
                      {'type': '天涯论坛', 'holder': 'http://bbs.tianya.cn/post-394-129735-1.shtml'})
    elif request.method == 'POST':
        address = request.POST['address']
        tianya_filter = TianyaFilter(address)
        title, topics = tianya_filter.start()
        return render(request, 'Portal/topic_filter.html',
                      {'type': '天涯论坛', 'address': address, 'title': title, 'result_list': topics})


def jiayuan(request):
    if request.method == 'GET':
        searcher = JiayuanSearcher()
        helper = JiayuanHelper(searcher)
        args = {'sex_dict': helper.sex_dict, 'region_dict': helper.region_dict, 'age_range': helper.age_range,
                'height_range': helper.height_range, 'education_dict': helper.education_dict,
                'income_dict': helper.income_dict, 'marriage_dict': helper.marriage_dict,
                'house_dict': helper.house_dict, 'car_dict': helper.car_dict, 'children_dict': helper.children_dict,
                'job_dict': helper.job_dict, 'blood_dict': helper.blood_dict, 'scope_dict': helper.scope_dict}
        return render(request, 'Portal/jiayuan.html', args)
    elif request.method == 'POST':
        searcher = JiayuanSearcher()
        searcher.login('yzj1995@vip.qq.com', '16777216')
        helper = JiayuanHelper(searcher)

        params = request.POST
        for key in params:
            if key.isdigit():
                helper.set_value(int(key), int(params[key]))

        helper.set_sex(params['sex'])

        age_from = 0
        age_to = 0
        if 'age_from' in params:
            age_from = params['age_from']
        if 'age_to' in params:
            age_to = params['age_to']
        helper.set_value(2, int(age_from), int(age_to))

        height_from = 0
        height_to = 0
        if 'height_from' in params:
            height_from = params['height_from']
        if 'height_to' in params:
            height_to = params['height_to']
        helper.set_value(3, int(height_from), int(height_to))

        labels, data = helper.start_single(int(params['item']))

        args = {'sex_dict': helper.sex_dict, 'region_dict': helper.region_dict, 'age_range': helper.age_range,
                'height_range': helper.height_range, 'education_dict': helper.education_dict,
                'income_dict': helper.income_dict, 'marriage_dict': helper.marriage_dict,
                'house_dict': helper.house_dict, 'car_dict': helper.car_dict, 'children_dict': helper.children_dict,
                'job_dict': helper.job_dict, 'blood_dict': helper.blood_dict, 'scope_dict': helper.scope_dict,
                'labels': json.dumps(labels), 'data': data}
        return render(request, 'Portal/jiayuan.html', args)
