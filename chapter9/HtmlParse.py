import re, json


class HtmlParser(object):
    ''' 网页解析器 '''

    def parse_url(self, page_url, response):
        '''
        提取当前页面正在上演的电影连接
        :param page_url:
        :param response:
        :return:
        '''
        pattern = re.compile(r'http://movie.mtime.com/\d+/')
        urls = pattern.findall(response)
        urls_list = list(set(urls)) if urls else None
        print(urls_list)
        return urls_list

    def parse_ajax(self, page_url, response):
        '''
        解析ajax响应
        :param page_url:
        :param response:
        :return:
        '''
        pattern = re.compile('.*?= (.*?);')
        result = pattern.findall(response)
        if result:
            value = json.loads(result[0])
            try:
                '''爬取的电影信息分为四种，已经上映的电影有票房成绩和没有票房成绩。
                还有就是即将上映，肯定没有票房成绩，最后一种是上映的时间久，肯定有票房'''
                ''' 所以按照票房成绩区分，即含有boxOffice字段和没有该字段两种情况 '''
                boxOffice = value.get('value').get('boxOffice')
            except Exception as e:
                print(e)
                return None
            if boxOffice:
                return self._parse_has_box(page_url, value)

            else:
                return self._parse_no_box(page_url, value)

    def _parse_has_box(self, url, value):
        '''
        解析有票房成绩的影片
        :param url: 电影url
        :param json_data: 返回的json数据
        :return:
        '''
        try:
            isRelease = value.get('value').get('isRelease')
            movieRating = value.get('value').get('movieRating')
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')
            TotalBoxOffice = boxOffice.get('TotalBoxOffice')
            TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
            TodayBoxOffice = boxOffice.get('TodayBoxOffice')
            TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')
            Rank = boxOffice.get('Rank')

            return (MovieId, movieTitle, RatingFinal,
                    ROtherFinal, RPictureFinal, RDirectorFinal,
                    RStoryFinal, Usercount, AttitudeCount,
                    TotalBoxOffice + TotalBoxOfficeUnit,
                    TodayBoxOffice + TodayBoxOfficeUnit,
                    Rank, isRelease)
        except Exception as e:
            print(e, url, value)
            return None

    def _parse_no_box(self, url, value):
        '''
        解析没有票房成绩的影片
        :param url: 解析电影url
        :param json_data: 返回的json数据
        :return:
        '''
        try:
            isRelease = value.get('value').get('isRelease')
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')
            Rank = 0

            return (MovieId, movieTitle, RatingFinal,
                    ROtherFinal, RPictureFinal, RDirectorFinal,
                    RStoryFinal, Usercount, AttitudeCount,
                    '',
                    '',
                    Rank, isRelease)
        except Exception as e:
            print(e, url, value)
            return None


if __name__ == '__main__':
    text = 'var result_20177281733978657 = { "value":{"isRelease":true,"movieRating":{"MovieId":229733,"RatingFinal":7.4,"RDirectorFinal":7.5,"ROtherFinal":6.9,"RPictureFinal":7.6,"RShowFinal":0,"RStoryFinal":6.6,"RTotalFinal":0,"Usercount":983,"AttitudeCount":5796,"UserId":0,"EnterTime":0,"JustTotal":0,"RatingCount":0,"TitleCn":"","TitleEn":"","Year":"","IP":0},"movieTitle":"战狼2","tweetId":0,"userLastComment":"","userLastCommentUrl":"","releaseType":1,"boxOffice":{"Rank":1,"TotalBoxOffice":"2.97","TotalBoxOfficeUnit":"亿","TodayBoxOffice":"1.94","TodayBoxOfficeUnit":"亿","ShowDays":2,"EndDate":"2017-07-28 21:20"}},"error":null};var movieOverviewRatingResult=result_20177281733978657;'
    parser = HtmlParser()
    data = parser.parse_ajax('http://movie.mtime.com/229733/', text)
    print(data)
    # (230647, '建军大业', -1, 0, 0, 0, 0, 0, 2221, '', '', 0, True)
    # (229733, '战狼2', 7.4, 6.9, 7.6, 7.5, 6.6, 983, 5796, '2.97亿', '1.94亿', 1, True)
