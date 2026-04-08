# -*-coding:utf-8 -*-
# Created: 07-06-2017 xuna
#   by Python 3.4.3  Sublime text 3(???)
#  _aurhor_ :xuna
import urllib.request ,sys
import re
import urllib.parse

# 使用默认值，避免交互式输入
provice = "北京"
city = "北京"
print(f"查询 {provice} {city} 的天气预报")
# 对URL中的中文字符进行编码
provice_encoded = urllib.parse.quote(provice)
city_encoded = urllib.parse.quote(city)
#?????url
url = "http://qq.ip138.com/weather/"+provice_encoded+'/'+city_encoded+'_7tian.htm'
print(f"请求URL: {url}")

#??????
weatherhtml = urllib.request.urlopen(url)
res = weatherhtml.read().decode('GB2312')

#???????
f=open('wea.txt','wb')
f.write(res.encode('GB2312'))
f.close()

print("保存HTML内容到 wea.txt 文件")
print("尝试提取天气信息...")

# 尝试提取标题
pattern = '<title>(.+?)</title>'
title_match = re.search(pattern, res)
if title_match:
    Title = title_match.group(1)
    print(f"标题: {Title}")
else:
    Title = f"{provice} {city} 天气预报"
    print(f"无法提取标题，使用默认标题: {Title}")

# 尝试提取日期和天气信息
# 这里使用更通用的模式，适应可能的HTML结构变化
date_pattern = '\d{4}-\d{2}-\d{2}'
date = re.findall(date_pattern, res)

# 尝试提取天气状况
weather_pattern = '<img[^>]+alt="([^"]+)"'
weather = re.findall(weather_pattern, res)

print ("%35.30s"%Title)
print("\n日期\t\t天气状况")
print("-" * 30)

# 确保日期和天气信息数量匹配
min_length = min(len(date), len(weather))
for i in range(min_length):
    print(f'{date[i]}\t{weather[i]}')

if min_length == 0:
    print("无法提取天气信息，可能网站结构已变化")
    print("请检查 wea.txt 文件了解网站当前结构")
