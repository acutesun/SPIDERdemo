from multiprocessing.managers import BaseManager
from HtmlParser import HtmlParser
from HtmlDownloader import HtmlDownloader


class SpiderWork(object):

    def __init__(self):
        # 使用Manager注册获取方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        server_addr = '127.0.0.1'
        print('connect to server %s' % server_addr)
        self.m = BaseManager(address=(server_addr, 8000), authkey='123'.encode('utf-8'))
        self.m.connect()
        self.task = self.m.get_task_queue()  # 获取任务队列
        self.result = self.m.get_result_queue()  # 结果队列
        # 初始化网页下载器和解析器
        self.parser = HtmlParser()
        self.downloader = HtmlDownloader()
        print('init finish')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print('crawl over!')
                        # 通知其他节点结束
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print('爬虫节点正在解析: %s' % url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({"new_urls": new_urls, "data": data})
            except EOFError as eofe:
                print('连接工作节点失败')
            except Exception as e:
                print(e.args)
                print('failed!')

if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()