import hashlib
import pickle


class UrlManager(object):
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt')
        self.old_urls = self.load_progress('old_urls.txt')

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
        m = hashlib.md5()
        m.update(new_url.encode('utf-8'))
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def add_new_url(self, url):
        '''
        :param url: 添加url到未爬取的urls集合, 使用md5压缩减少内存占用
        :return:
        '''
        if url is None:
            return
        m = hashlib.md5()
        print(url)
        m.update(url.encode('utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
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

    def save_progress(self, path, data):
        '''
        保存进度
        :param filename: 文件路径
        :param data: 数据
        :return:
        '''
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        '''
        从本地文件加载urls集合
        :param path: 文件路径
        :return: urls集合
        '''
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except Exception:
            print('无进度文件')
        return set()