# Web-Scraping

Headers
1、	为什么要设置headers? 
import requests
res=requests.get("http://www.dianping.com/",headers=headers)
print(res.text)
#抱歉！页面无法访问...
在使用python爬虫爬取数据的时候，经常会遇到一些网站的反爬虫措施，一般就是针对于headers中的User-Agent，如果没有对headers进行设置，User-Agent会声明自己是python脚本，而如果网站有反爬虫的想法的话，会拒绝这样的连接。在请求网页爬取的时候，输出的text信息中会出现抱歉，无法访问等字眼。而修改headers可以将自己的爬虫脚本伪装成浏览器的正常访问，来避免这一问题。

2、 headers在哪里找？ 
谷歌或者火狐浏览器，在网页面上点击右键，检查（F12是快捷键），剩余按照图中显示操作，需要刷新网页。
疑问：不同浏览器出来的header不一样？
Data: F12-Network-signin/logon-fresh-headers-Fromdata/other
 
3、headers中有很多内容，主要常用的就是user-agent 和 host，他们是以键对的形式展现出来，如果user-agent 以字典键对形式作为headers的内容，就可以反爬成功，就不需要其他键对；否则，需要加入headers下的更多键对形式。

import urllib, urllib2
def get_page_source(url):
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               'Referer': 'http://www.baidu.com/'
               }
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    page_source = response.read()
return page_source



HTML
html.text
html.links
html.absolute_links


Get html in different libraries
1.	requests
import requests
headers={
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}
response = requests.get("http://www.dianping.com/",headers=headers)
html = response.text
soup = BeautifulSoup(html, 'lxml')

2.	urllib
from urllib.request import urlopen
html = urlopen(url).read().decode('utf-8')


3.	urllib2
无法安装，暂时无法检测
import urllib2
response = urllib2.Request(url, headers=headers)
html = urllib2.urlopen(response, date=None, timeout).read() #html_clip


Parse html
1.	BeautifulSoup

2.	lxml: python的HTML/XML的解析器
1)	etree.HTML(html_clip): 将字符串格式的 html 片段解析成可用于xpath的 html 文件
from lxml import etree

html_clip = '''
    <p>
      <ul> 
<li class="item-0"><a href="link1.html"><span>first item</span></a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>
       </ul>
     </p>
'''
# html_clip here = response.text/html in the above ‘gethtml’ part, which is ‘html’ clip, is a object of Python.
html_document = etree.HTML(html_clip)
result = etree.tostring(html_document).decode('utf-8')
result结果为：str类型，经过处理之后li节点标签被补全，自动添加了body、html 节点。
<Element html at 0x39e58f0>
<html><body><p>
      <ul>
          <li class="item-0"><a href="link1.html"><span>first item</span></a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>       
</li></ul>
     </p>
 </body></html>
 

使用parse打开html的文件
html_document = etree.parse('html_clip.html', etree.HTMLParser()) 
#此html_document可以使用.xpath
result = etree.tostring(html_document,pretty_print=True).decode('utf-8')
print(result)
result结果为（未验证）：li 节点标签被补全。
<html><body><p>
   <ul>
      <li class="item-0"><a href="link1.html"><span>first item</span></a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>       
</li></ul>
</p></body></html>

2)	xpath: 选取所有符合要求的标签的内容。注意：如果获取a标签的所有内容，a后面就不用再加正斜杠，否则报错。
//*	所有节点

html_document = etree.HTML(html_clip)
html_data = html_document.xpath('/html/body/p/ul/li/a') 
#html_data是列表形式，其每一个元素都是一个 Element 对象，需要遍历
for i in html_data:
    print(i.text)
#or
html_data = html_document.xpath('/html/body/p/ul/li/a/text()')
for i in html_data:
print(i)

#相对路径
html_data = html_document.xpath('//li/a/text()') 
//text( )	所有子孙节点的文本 same as /descendant::text()
first item
second item
third item
fourth item
fifth item
#疑问：输出为空？为啥？包括链家项目里li中使用class项也是输出为空，其他属性都可以
疑问：为什么有时候xpath刚开始输出为空，过一会又好了
 

属性值获取
html_data = html_document.xpath('/html/body/p/ul/li/a/@href') 
for i in html_data:
print(i)

#相对路径
html_data = html_document.xpath('//li/a//@href') #or /@href ('//li/a/@href ')
# // or / ?
link1.html
link2.html
link3.html
link4.html
link5.html


属性匹配
html_data = html_document.xpath('/html/body/p/ul/li/a[@href="link2.html"]/text()')
print(html_data) #['second item']
#相对路径下(非从根开始查找）属性匹配
html_data=html_document.xpath('//li/a[@href="link1.html"]')
两属性之间加and、or

属性多值匹配
html_clip = '''
<li class="li li-first"><a href="link.html">first item</a></li>
'''
html_document = etree.HTML(html_clip)
html_data = html_document.xpath ('//li[contains(@class, "li")]/a/text()')


按序选择：注意这里和代码中不同，序号是以 1 开头的，不是 0 开头的。
html_data = html_document.xpath('//li[1]/a/text()')
查找最后一个li标签里的a标签的文本内容
html_data = html_document.xpath('//li[last()]/a/text()')
查找倒数第二个li标签里的a标签的文本内容
html_data = html_document.xpath('//li[last()-1]/a/text()')
查找位置小于 3 的 li 节点，也就是位置序号为 1 和 2 的节点
html_data = html_document.xpath('//li[position()<3]/a/text()')


已知子节点，使用 .. 来获取父节点
html_data = html_document.xpath('//a[@href="link4.html"]/../@class') #['item-1']
通过 parent:: 来获取父节点
html_data = html_document.xpath ('//a[@href="link4.html"]/parent::*/@class')

Eg: 
<span class="spanClass">NAME: </span>JOHN<i class="remove"></i>
//a/span[contains(text(),'NAME')]/text() | //a/span[contains(text(),'NAME')]/../text() # NAME: JOHN

节点轴XPath Axes，包括获取子元素、兄弟元素、父元素、祖先元素等
ancestor轴获取所有祖先节点，其后需要跟两个冒号，然后是节点的选择器，这里*，表示匹配所有节点，因此返回结果是第一个li节点的所有祖先节点，包括html，body，div，ul。
result = html_document.xpath('//li[1]/ancestor::*') #Element对象为元素的列表
添加限定条件，这里在冒号后面加了div，得到的结果是div这个祖先节点。
result = html_document.xpath('//li[1]/ancestor::div')
attribute 轴可以获取所有属性值，其后跟的选择器*代表返回li节点的所有属性值。
result = html_document.xpath('//li[1]/attribute::*') # ['item-0']
child 轴可以获取所有直接子节点，这里限定条件是选取 href 属性为 link1.html 的a节点。
result = html_document.xpath('//li[1]/child::a[@href="link1.html"]')
descendant 轴可以获取所有子孙节点，这里限定条件获取span节点，所以返回的就是只包含span节点而没有a节点。
result = html_document.xpath('//li[1]/descendant::span')
following 轴可以获取当前节点之后的所有节点，*匹配+索引选择，获取了第二个后续节点。
result = html_document.xpath('//li[1]/following::*[2]')
following-sibling 轴可以获取当前节点之后的所有同级节点，*匹配获取所有后续同级节点。
result = html_document.xpath('//li[1]/following-sibling::*')

参考：https://zhuanlan.zhihu.com/p/29436838

Eg: Extract the number based on the span text
<div class="info">
    <p>
        <i class="icon-trending-up"></i>
        <span>Rank:</span>
        600
    </p>
</div>
item['rank'] = ''.join(s.strip() for s in html_document.xpath('//div//span[contains(., "Rank:")]/ancestor::p/text()').extract()) #600

item["rank"] = response.xpath('//span[.="Rank:"]/following-sibling::text()[1]').extract_first() #未验证



/node()	To get any child node











如果在提取某个页面的某个标签的xpath路径的话，可以如下图：
 
//*[@id="kw"]
解释：使用相对路径查找所有的标签，属性id等于kw的标签。


3.	Scrapy
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.http import HtmlResponse
html_clip = """<!DOCTYPE html>
<html>
  <head lang="en">
    <meta charset="UTF-8">
    <title></title>
  </head>
  <body>
    <ul>
      <li class="item-"><a id='i1' href="link.html" rel="external nofollow" >first item</a></li>
      <li class="item-0"><a id='i2' href="llink.html" rel="external nofollow" >first item</a></li>
      <li class="item-1"><a href="llink2.html" rel="external nofollow" rel="external nofollow" >second item<span>vv</span></a></li>
    </ul>
    <p><a href="llink2.html" rel="external nofollow" rel="external nofollow" >second item</a></p>
  </body>
</html>
"""
response = HtmlResponse(url='http://example.com', body=html, encoding='utf-8')
hxs = HtmlXPathSelector(response)
print(hxs)
# hxs = Selector(response=response).xpath('//a')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[2]')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[@id]')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[@id="i1"]')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[@href="link.html" rel="external nofollow" rel="external nofollow" ][@id="i1"]')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[contains(@href, "link")]')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[starts-with(@href, "link")]')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[re:test(@id, "i\d+")]')
# print(hxs)
# hxs = Selector(response=response).xpath('//a[re:test(@id, "i\d+")]/text()').extract()
# print(hxs)
# hxs = Selector(response=response).xpath('//a[re:test(@id, "i\d+")]/@href').extract()
# print(hxs)
# hxs = Selector(response=response).xpath('/html/body/ul/li/a/@href').extract()
# print(hxs)
# hxs = Selector(response=response).xpath('//body/ul/li/a/@href').extract_first()
# print(hxs)
  
# ul_list = Selector(response=response).xpath('//body/ul/li')
# for item in ul_list:
#   v = item.xpath('./a/span')
#   # 或
#   # v = item.xpath('a/span')
#   # 或
#   # v = item.xpath('*/a/span')
#   print(v)



4.	Regular Expression
参考：https://blog.csdn.net/Eastmount/article/details/51082253
1)	<tr></tr>标签
res_tr = r'<tr>(.*?)</tr>'
m_tr =  re.findall(res_tr,html_clip,re.S|re.M) #html_clip is a string
for line in m_tr: # m_tr is a list of string
    print (line) # or print (unicode(line,'utf-8')) #防止乱码
findall(string[, pos[, endpos]]) | re.findall(pattern, string[, flags]): 搜索string，以列表形式返回全部能匹配的子串。其中RE的常见参数包括：
re.I(re.IGNORECASE): 忽略大小写（括号内是完整写法）
re.M(re.MULTILINE): 多行模式，改变'^'和'$'的行为
re.S(re.DOTALL): 点任意匹配模式，改变'.'的行为


2)	<a href..></a>超链接
html_clip = '''
<td>
<a href="https://www.baidu.com/articles/zj.html" title="浙江省">浙江省主题介绍</a>
<a href="https://www.baidu.com//articles/gz.html" title="贵州省">贵州省主题介绍</a>
</td>
'''
#获取链接文本内容: <a href></a>之间
text =  re.findall(r'<a .*?>(.*?)</a>', html_clip, re.S|re.M) #疑问：小括号的作用是不是选取匹配的对象？
for value in text: print (value) #浙江省主题介绍 贵州省主题介绍
 
#获取完整a标签内容
urls=re.findall(r"<a.*?href=.*?<\/a>", html_clip, re.I|re.S|re.M)
for i in urls: print (i)
# <a href="https://www.baidu.com/articles/zj.html" title="浙江省">浙江省主题介绍</a>
<a href="https://www.baidu.com//articles/gz.html" title="贵州省">贵州省主题介绍</a>
 
#获取<a href></a>中的URL
res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
#pattern to find: 前面是href=", 后面是", 此对象是任意字符, 1次或无限次, 不知道是否存在
link = re.findall(res_url, html_clip, re.I|re.S|re.M)
for url in link: print (url)
  

3)	图片URL
urls = "http://i1.hoopchina.com.cn/blogfile/201411/11/BbsImg141568417848931.jpg"
values = urls.split('/')[-1] # BbsImg141568417848931.jpg

4)	爬取网页title：通常位于<html><head><title>标题</title></head></html>中
from urllib.request import urlopen
html = urlopen("http://www.csdn.net/").read().decode('utf-8')

pat_compiled = re.compile(r'(?<=<title>).*?(?=</title>)',re.M|re.S) 
title_obj = re.search(pat_compiled, html) #or title_obj = pat_compiled.search(html) 
# <_sre.SRE_Match object; span=(449, 462), match='CSDN-专业IT技术社区'>
title = title_obj.group() #['CSDN-专业IT技术社区']
#Second method
title = re.findall(r'<title>(.*?)</title>', html) #['CSDN-专业IT技术社区']

5)	定位table位置并爬取属性-属性值
<table class="infobox" >  
<tr>  
<td>序列号</td><td>DEIN3-39CD3-2093J3</td>  
<td>日期</td><td>2013年1月22日</td>  
<td>售价</td><td>392.70 元</td>  
<td>说明</td><td>仅限5用户使用</td>  
</tr>  
</table>  
start = language.find(r'<table class="infobox"')
end = language.find(r'</table>') 
infobox = language[start:end] 
m = re.findall(r'<td>(.*?)</td><td>(.*?)</td>',infobox,re.S|re.M)  
for line in m:  
    print (line[0],line[1])

6)	通过replace函数过滤<br />标签（表示HTML换行）
if '<br />' in value:
   value = value.replace('<br />','')   #过滤该标签
   value = value.replace('\n',' ')      #换行空格替代

7)	过滤所有标签
value = re.sub('<[^>]+>','', html) #用''替换所有< >格式的标签
 
