# http://seputu.com/ 爬取盗墓笔记
import requests
from lxml import etree
import json
import csv

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'user-agent': 'user_agent'}
response = requests.get('http://seputu.com/', headers=headers)
html = etree.HTML(response.text)
# html = etree.parse('2.html')   # 解析本地文件

titles = html.xpath('//div[@class="mulu-title"]//h2')
chapters = html.xpath('//div[@class="box"]//a')
print(chapters)
content = []
for chapter in chapters:
    # print(chapter.text, chapter.xpath('@href'))
    title = chapter.text        # 获取当前元素的内容
    url = chapter.xpath('@href')  # 获取当前元素的href属性
    obj = {
        'title': title,
        'url': url
    }
    content.append(obj)
with open('1.json', 'w') as f:
    json.dump(content, f, indent=5, ensure_ascii=False)  # 存储为json

header = ['id', 'title', 'url']
with open('daomubiji.csv', 'w') as f:  # 存储为csv
    f_csv = csv.DictWriter(f, header)
    f_csv.writeheader()
    f_csv.writerows(content)

