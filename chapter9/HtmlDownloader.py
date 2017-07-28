import requests

class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        headers = {
            'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None