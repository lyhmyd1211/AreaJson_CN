# -*- coding: UTF-8 -*-

import json
import urllib.request
# import requests
import urllib.parse
import ssl
import os
import time
from bs4 import BeautifulSoup

# config #

year = '2020'       # 年份，目前国家统计局官网有2009-2019年的数据
level = 3           # 可选：3|5   获取的层级 3层为省-市-区  最多5级省-市-区-县（街道）-乡镇（居委会）
digit = 6           # 可选：6|12  行政区划代码位数  层级为3级时通常使用6位代码 如110000,层级为5级时使用12位代码 如 110000000000
head_url = "index"  # 可选：index|各省行政区划前两位  要从哪开始获取 index为全国所有省份  要获取单独的省份修改为省行政区划的前两位

# config #


context = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
mainUrl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'
attrsClassArr = ['provincetr', 'citytr', 'countytr', 'towntr', 'villagetr']


def is_CN(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def retry(times):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            i = 0
            while i < times:
                try:
                    if i > 0:
                        print('正在尝试第%d次请求' % (i+1))
                    return func(*args, **kwargs)
                except:
                    #	此处打印日志  func.__name__ 为say函数
                    print('%s 请求失败!' % (args[0]))
                    # print("logdebug: {}()".format(func.__name__))
                    i += 1
        return inner_wrapper
    return wrapper


@retry(5)
def fetchAreaData(url, index, attrsClass, area):
    if index < level:
        try:
            with urllib.request.urlopen(url, context=context, timeout=3) as response:
                soup = BeautifulSoup(response.read(), 'html.parser')
                tag = soup.find_all(attrs={"class": attrsClass})
                for tg in tag:
                    villageArr = []
                    for tgc in tg.children:
                        if tgc.a:
                            if is_CN(tgc.a.get_text()):
                                print('正在请求', '/'.join(url.split('/')
                                                       [0:-1]) + '/' + tgc.a.attrs['href'], tgc.a.get_text())
                                if index + 1 == level:
                                    area.append(
                                        {"value": tgc.a.attrs['href'].split('/')[-1].replace('.html', '').ljust(digit, '0'), "label": tgc.a.get_text()})
                                else:
                                    content = {"value": tgc.a.attrs['href'].split(
                                        '/')[-1].replace('.html', '').ljust(digit, '0'), "label": tgc.a.get_text(), "children": []}
                                    area.append(content)
                                    fetchAreaData(
                                        '/'.join(url.split('/')[0:-1]) + '/' + tgc.a.attrs['href'], index+1, attrsClassArr[index+1], area[len(area)-1]['children'])
                        elif attrsClass == 'villagetr':
                            villageArr.append(tgc.get_text())
                    if len(villageArr) > 0:
                        area.append(
                            {"value": villageArr[0], "label": villageArr[2]})
        except urllib.request.URLError as e:
            print("出现异常: "+str(e))


position = 0
areas = []
if head_url != 'index':
    position = 1

fetchAreaData(mainUrl+year+'/'+head_url+'.html',
              position, attrsClassArr[position], areas)
with open(head_url+'_'+year+'_'+"_level_" + str(level)+'.json', "w", encoding='utf-8') as json_file:
    json.dump(areas, json_file, ensure_ascii=False)
    print("写入%s完成" % (head_url+'_'+year+'_'+"_level_" + str(level)+'.json'))


# code = ['11', '12', '13', '14', '15', '21', '22','23', '31', '32', '33', '34', '35', '36', '37',
#         '41', '42', '43', '44', '45', '46', '50', '51', '52', '53', '54', '61', '62', '63', '64', '65']
# for index in range(24):
#     areas = []
#     head_url = code[index]
#     position = 0
#     if head_url != 'index':
#         position = 1
#     fetchAreaData(mainUrl+year+'/'+head_url+'.html',
#                   position, attrsClassArr[position], areas)
#     with open('province/level_5/'+head_url+'_'+year+'_'+"_level_" + str(level)+'.json', "w", encoding='utf-8') as json_file:
#         json.dump(areas, json_file, ensure_ascii=False)
#         print("写入%s完成" % (head_url+'_'+year+'_'+"_level_" + str(level)+'.json'))
