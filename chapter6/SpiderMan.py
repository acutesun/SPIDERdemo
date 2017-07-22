from HtmlDownloader import HtmlDownloader
from Dataouput import DataOutput
from HtmlParser import HtmlParser
from URLManager import URLManager


class SpiderSchedule(object):
    '''
    爬虫调度器，负责初始化各个模块，然后通过crawl传递入口url
    方法内部安卓运行流畅控制各个模块工作
    '''
    def __init__(self):
        self.manager = URLManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 添加入口url
        self.manager.add_new_url(root_url)
        # 判断是否有新的url，同时判断抓取url个数
        while self.manager.has_new_url() and self.manager.old_urls_size() < 10:
            try:
                # 1.从URL管理器获取新的URL
                new_url = self.manager.get_new_url()
                # 2.将URL交给HtmlDownloader下载
                html = self.downloader.download(new_url)
                # 3.将下载的页面交给HtmlParser解析
                urls, data = self.parser.parser(new_url, html)
                # 4.将解析的数据存储，将重新抽取的URL交给URLManager
                self.output.store_data(data)
                for url in urls:
                    self.manager.add_new_url(url)
                print('已经抓取{0}个链接:'.format(self.manager.old_urls_size()), new_url)
            except Exception as e:
                print(e.args)
                print('crawl failed:', url)
        self.output.output_html()

if __name__ == '__main__':
    schedule = SpiderSchedule()
    schedule.crawl('http://baike.baidu.com/view/284853.htm')
