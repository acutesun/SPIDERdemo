import codecs


class DataOutput(object):

    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        print('store_data:', len(self.datas))
        self.datas.append(data)


    def output_html(self):
        fout = codecs.open('baike.html', 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        count = 0
        for data in self.datas[:]:
            count += 1
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>%s</td>" % data['summary'])
            fout.write("</tr>")
            self.datas.remove(data)
        fout.write("<h1>{0}</h1>".format(count))
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</ht>")
