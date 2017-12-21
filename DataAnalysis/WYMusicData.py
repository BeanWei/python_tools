# -*- coding: utf-8 -*-
# bulid by Bean_Wei/ 2017/12/12 21:35

from selenium import webdriver
import time
import MySQLdb
from bs4 import BeautifulSoup
import re
from pyecharts import Bar
from pyecharts import WordCloud
from pyecharts import Page
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf8')
'''
#连接数据库
conn=MySQLdb.connect("localhost","root","1204","wymusicdata" ,charset="utf8")
cur=conn.cursor()
print "连接数据库成功"
'''
x=webdriver.Chrome() #不能少了括号
page=0
listenNums=[]
songLists=[]
authors=[]
#网易云音乐网页采用了框架，需要爬取的歌单在iframe里面，
# 这种情况我们直接定位是不能定位到元素，
# 采用x.switch_to_frame（“”）进入框架进行数据爬取
while True:
    x.get('http://music.163.com/discover/playlist/?offset=%s' % page)
    #x.get('http://music.163.com/discover/playlist/?offset=210')
    x.switch_to_frame(x.find_element_by_name("contentFrame"))
    html=x.page_source
    soup=BeautifulSoup(html,"html.parser")
    #精确定位找到我们需要的<li>标签内容
    cm=soup.find(class_="m-cvrlst f-cb")
    contents=cm.find_all('li')
    for content in contents:
        wan=str(content)
        if "万" in wan:
            wan=wan.replace('万',"0000")
        else:
            wan=wan
        listenNum=re.findall(r'<span class=\"nb\">(.*?)</span>',str(wan))
        #songList=re.findall(r'<a class=\"tit f-thide s-fc0\" href=".*?" title="(\".*\")">',str(content))
        songList=content.find(class_="tit f-thide s-fc0").text
        #author=re.findall(r'<a class=\"nm nm-icn f-thide s-fc3\" href=".*?" title=".*?">(.*?)</a>',str(content))
        author=content.find(class_="nm nm-icn f-thide s-fc3").text
        #取出来的元素放进列表
        listenNums.append(listenNum[0])
        songLists.append(songList)
        authors.append(author)

    #到浏览到最后一页时("js-disabled")=下一页无法点击 即认为 爬取完成
    if page!=0:
        try:
            x.find_element_by_class_name("js-disabled")
            print "全部歌单爬取成功"
            break
        except:
            print "已成功爬取第%s页"% (page/35+1)
            pass

    page+=35
    # if page==70:
    #     break
    time.sleep(2)
    #由于网易云音乐网站在底部有个播放器的小元素导致无法点击下一页
    # try:
    #     x.find_element_by_class_name("znxt").click()
    #     time.sleep(2)
    # except:
    #     print "全部歌单爬取成功"
    #     break
    #在这里只能采用分析歌单的url，遍历所有的连接来代替点击下一页
    #--------------------------------------------

#歌单名字做词频统计绘制词云图
ciyun=''
for words in songLists:
    #rfw=re.match("([\u4e00-\u9fa5])",words)
    pattern =re.compile(u"[\u4e00-\u9fa5]+")
    result=re.findall(pattern,words)
    for r in  result:
        word=jieba.cut(r)
        if ciyun!='':
            ciyun=ciyun+','+",".join(word)
        else:
            ciyun+=",".join(word)
ciyunList=ciyun.split(",")
dict={}
for i in ciyunList:
    if i not in dict:
        dict[i]=1
    else:
        dict[i]+=1
key=[]
value=[]
for k,v in dict.items():
    key.append(k)
    value.append(v)

#page=Page()
bar=Bar("网易Music","网易云音乐歌单热度")
bar.add("歌单热度",songLists,listenNums,mark_point=["max", "min"])
#page.add(bar)
bar.render()
'''
wordcloud=WordCloud("歌单名词云",width=600,height=800)
wordcloud.add("",key,value,word_size_range=[20,100],shape="cardioid")
page.add(wordcloud)
#page.render()
'''
#词云
bgImage=plt.imread('xin.jpg')
wc=WordCloud(background_color='black',
             mask=bgImage,
             font_path='simkai.ttf',
             max_font_size=50,
             random_state=30,
             )
wc.generate(ciyun)
plt.imshow(wc)
wc.to_file("WYsongLciyun.png")