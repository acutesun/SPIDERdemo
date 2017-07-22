# 5.3 email 提醒
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from lxml import etree


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 发件人地址
from_addr = 'blurredsun@sina.com'
password = 'xl133519SXG'
to_addr = 'sxgjob@163.com'
smtp_server = 'smtp.sina.com'  # 邮箱服务器地址
# 设置邮件信息
# msg = MIMEText('运行异常, 状态码 404', 'plain', 'utf-8')  # pain 表示存文本
html_elem = etree.parse('2.html')
html = etree.tostring(html_elem)
msg = MIMEText(html, 'html', 'utf-8')  # html表示html

msg['From'] = _format_addr('一号爬虫 <%s>' % from_addr)
msg['to'] = _format_addr('管理员 <{0}>'.format(to_addr))
msg['Subject'] = Header('一号爬虫运行状态', 'utf-8')
# 发送邮件
server = smtplib.SMTP(smtp_server, 25)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
