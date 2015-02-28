from django.shortcuts import render
from Portal.helpers.loop_requester import LoopSpider
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
        return render(request, 'Portal/loop_spider.html', { 'result_list': record })