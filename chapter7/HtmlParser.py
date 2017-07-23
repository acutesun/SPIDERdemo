from urllib.request import urljoin
from lxml import etree
from HtmlDownloader import HtmlDownloader


class HtmlParser(object):

    def parser(self, page_url, html_content):
        flag = page_url and html_content
        if flag:
            urls = self._get_new_url(page_url, html_content)
            data = self._get_new_data(page_url, html_content)
            return urls, data
        return None

    def _get_new_url(self, page_url, html_content):
        '''
        抽取当前界面的urls
        :param page_url: 当前页面url
        :param html_content: 当前html
        :return: 抽取的urls集合
        '''
        html = etree.HTML(html_content)
        links = html.xpath('//a/@href')
        new_urls = set()
        for link in links:
            link = urljoin(page_url, link)
            if 'item' in link or 'view' in link:
                new_urls.add(link)
        return new_urls

    def _get_new_data(self, page_url, html_content):
        '''
        抽取当前界面数据
        :param page_url: 当前页面url
        :param html_content: 当前html
        :return: 返回收取数据
        '''
        html = etree.HTML(html_content)
        titles = html.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]//h1')
        title = titles[0].text if titles else ''
        summary_list = html.xpath('//div[@class="lemma-summary"]//*')  # 提取摘要
        summary = ''
        for sum in summary_list:
            sum.tail = sum.tail if sum.tail else ''
            sum.text = sum.text if sum.text else ''
            summary += sum.text + sum.tail
        # print(title[0].text, text)
        data = {}
        data['url'] = page_url
        data['title'] = title
        data['summary'] = summary
        return data


if __name__ == '__main__':
    parser = HtmlParser()
    downloader = HtmlDownloader()
    url = "http://baike.baidu.com/view/284853.htm"
    urls = parser._get_new_data(url, downloader.download(url))
