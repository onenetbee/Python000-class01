"""
Python训练营作业一
Function：测试json
"""

from lxml import etree
import requests
import json
from time import sleep

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/78.0.3904.108 Safari/537.36 '
header = {'user-agent': user_agent}

url = f'http://httpbin.org'
html = requests.get(url, headers=header)
s = etree.HTML(html.text)
trs = s.xpath('///text()')
print(trs)
json_str = json.dumps(trs)
print("JSON 对象：", json_str)
response = requests.post('https://httpbin.org/post', headers=header, data=json_str)
print(response.text)
