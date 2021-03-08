# AreaJson_CN

## (已更新 2020 年数据)

## 最新中国省市区县乡镇 5 级行政区划代码<br/>

#### index_2020_level_3.json：全国省市区 3 级 6 位行政区划代码<br/>

#### index_2020_level_5.json：全国省市区县乡镇 5 级 12 位行政区划代码<br/>

#### province 文件夹是全国各省行政区划代码（文件名开头的两位数为各省行政区划代码前两位）<br/>

##### province/level_3 为各省 3 级 6 位行政区划代码

##### province/ level_5 为各省 5 级 12 位行政区划代码

数据来源：[国家统计局](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/)

getArea.py 为简易的爬虫脚本,需要修改爬取内容的见脚本说明

## 脚本说明:<br/>

```
# config #

year = '2012'       # 年份，目前国家统计局官网有2009-2019年的数据
level = 3           # 可选：3|5   获取的层级 3层为省-市-区  最多5级省-市-区-县（街道）-乡镇（居委会）
digit = 6           # 可选：6|12  行政区划代码位数  层级为3级时通常使用6位代码 如110000,层级为5级时使用12位代码 如 110000000000
head_url = "index"  # 可选：index|各省行政区划前两位  要从哪开始获取 index为全国所有省份  要获取单独的省份修改为省行政区划的前两位

# config #
```

按照注释修改 config 中的内容再运行脚本可以获取自己想要的结果

[最新中国省市区县 geoJSON 格式地图数据的点这里](https://github.com/lyhmyd1211/GeoMapData_CN)
