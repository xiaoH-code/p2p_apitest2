from bs4 import BeautifulSoup

html = """
<html>
<head><title>黑马程序员</title></head>
<body>
    <p id="test01">软件测试</p>
    <p id="test02">2020年</p>
    <a href="/api.html">接口测试</a>
    <a href="/web.html">Web自动化测试</a>
    <a href="/app.html">APP自动化测试</a>
</body>
</html>
"""

bs = BeautifulSoup(html,"html.parser")

print(bs.title)
print(bs.title.name)
print(bs.title.string)

print(bs.p)
print(bs.p['id'])
print(bs.p.string)

print(bs.find_all('p'))

for a in bs.find_all('a'):
    print('a href={} text={}'.format(a['href'],a.string))
    print('a href={} text={}'.format(a.get('href'),a.get_text()))

