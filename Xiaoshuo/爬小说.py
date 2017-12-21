# -*- coding: utf-8 -*-
# bulid by Bean_Wei/ 2017/11/28 7:48

import random
from bs4 import BeautifulSoup
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


head_user_agent=['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                 'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                 'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                 'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                 'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                 'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                 'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
header={'User-Agent':head_user_agent[random.randrange(0,len(head_user_agent))]}

def getNovelUrlList():
    while True:
        try:
            novelname=raw_input("请输入小说名或关键字: ")
            url='http://zhannei.baidu.com/cse/search?s=920895234054625192&entry=1&q=%s' % urllib2.quote(novelname)
            res=urllib2.Request(url,headers=header)
            html=urllib2.urlopen(res).read().decode('utf-8')
            reg=r'<a cpos="title" href="(.*?)" title="(.*?)" class=".*?" target=".*?">'
            NovelUrlList=re.findall(reg,html)
            if  NovelUrlList!=[]:
                break
        except:
            print "请重新输入"
    return NovelUrlList
def getNovelContent(url):
    res=urllib2.Request(url,headers=header)
    html=urllib2.urlopen(res).read().decode('utf-8')
    reg=r'<dd> <a style="" href="(.*?)">(.*?)</a></dd>'
    reg2=r'<h1>(.*?)</h1>'
    NovelChapter=re.findall(reg,html)
    NovelName=re.findall(reg2,html)[0]
    file = open('%s.txt'%NovelName, 'w')
    for NovelChapterUrl in NovelChapter:
        url="http://www.qu.la"+NovelChapterUrl[0]
        res=urllib2.Request(url,headers=header)
        page=urllib2.urlopen(res).read().decode('utf-8')
        soup=BeautifulSoup(page,"html.parser")
        NovelContent=soup.find('div',id="content").get_text()
        Content="=*=*="*18+'\n'+NovelChapterUrl[1]+"\n\n"+NovelContent
        print "正在下载 =========%s=======》》》》》》%s" % ( NovelName,NovelChapterUrl[1])
        file.write(Content)
        file.flush()
    file.close()

NovelUrlList=getNovelUrlList()
n=0
for name in NovelUrlList:
    n+=1
    print str(n)+"."+name[1]
while True:
    try:
        num=raw_input("请选择：")
        SelectUrl=NovelUrlList[int(num)-1][0]
        if SelectUrl!=' ':
            break
    except:
        print "输入有误，请重新输入"
getNovelContent(SelectUrl)


