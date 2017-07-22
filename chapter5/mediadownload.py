# 5.2 多媒体文件下载
from urllib.request import urlretrieve
from urllib import parse
from lxml import etree
import requests


def Schedule(blocknum, blocksize, totalsize):
    '''
    :param blocknum: 已经下载的数据块
    :param blocksize: 数据块的大小
    :param totalsize: 远程文件的大小
    :return:
    '''
    per = 100.0 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    print('当前下载进度：', per)


def download():
    headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    response = requests.get('http://bizhi.sogou.com/cate/index/4?f=nav', headers=headers)
    html = etree.HTML(response.text)
    image_urls = html.xpath('//img/@src')
    print(image_urls)
    i = 0
    for image_url in image_urls:
        print('正在下载：', image_url)
        if not image_url.startswith('http'):
            image_url = parse.urljoin(response.url, image_url)
        urlretrieve(image_url, 'image'+str(i)+'.jpg', Schedule)
        i += 1


if __name__ == '__main__':
    download()
