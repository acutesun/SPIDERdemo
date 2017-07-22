

class URLManager(object):
    '''
    url管理器, 主要包含两个集合，一个是已经爬取的url集合，另外一个是未爬取的url集合
    '''
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        '''
        :return: 是否有未爬取的url
        '''
        return self.new_urls_size() != 0

    def get_new_url(self):
        '''
        :return: 返回一个未爬取的url
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        '''
        :param url: 添加url到未爬取的urls集合
        :return:
        '''
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def new_urls_size(self):
        '''
        :return: 未爬取url集合大小
        '''

        return len(self.new_urls)

    def old_urls_size(self):
        '''
        :return: 已爬取url集合大小
        '''
        return len(self.old_urls)

    def get_old_ulrs(self):
        return self.old_urls
