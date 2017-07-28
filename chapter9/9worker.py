import time, re

from Dataoutput import DataOut
from HtmlParse import HtmlParser
from HtmlDownloader import HtmlDownloader


class SpiderWork(object):
    def __init__(self):
        self.dataout = DataOut()
        self.parser = HtmlParser()
        self.downloader = HtmlDownloader()

    def crawl(self, root_url):
        content = self.downloader.download(root_url)
        urls = self.parser.parse_url(root_url, content)

        for url in urls:
            t = time.strftime('%Y%m%d%H%M', time.localtime())
            try:
                movie_id = ''
                mobj = re.match(r'.*?/(\d+)/.*?', url)
                if mobj:
                    movie_id = mobj.group(1)
                # print(movie_id)
                ajax_url = '''http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.
                            Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CrossDomain=1&
                            Ajax_RequestUrl={0}&t={1}&Ajax_CallBackArgument0={2}'''.format(url, t,
                                                                                           movie_id)  # 构造ajax的url
                ajax_content = self.downloader.download(ajax_url)  # 获取ajax响应内容
                data = self.parser.parse_ajax(ajax_url, ajax_content)  # 解析出数据
                self.dataout.store_data(data)
                print('crawling: ', ajax_url)
            except Exception as e:
                print('crawl failed: ', url, e)
        self.dataout.output_end()
        print('crawl finish!')


if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl('http://theater.mtime.com/China_Beijing')