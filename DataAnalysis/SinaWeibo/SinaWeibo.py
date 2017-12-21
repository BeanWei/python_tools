# -*- coding: utf-8 -*-
# bulid by Bean_Wei/ 2017/11/30 22:17

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from PIL import Image
import re
import time
import getpass #隐藏输入的字符（PyCharm 不支持QAQ）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

print "脚本：SinaWeibo脚本\n作者：Bean.Wei\n功能: 多得一批"
#x=webdriver.PhantomJS()
x=webdriver.Chrome()

#登陆新浪微博
def loadingWeibo():
    loginUrl='https://login.sina.com.cn/signup/signin.php'
    #x.delete_all_cookies()
    x.get(loginUrl)
    time.sleep(5)
    while True:
        if x.current_url != loginUrl:
            break
        username=raw_input("账号：")
        password=raw_input("密码：")
        #password=getpass.getpass("密码：")
        x.find_element_by_id('username').clear()
        x.find_element_by_id('username').send_keys(username)
        x.find_element_by_id('password').clear()
        x.find_element_by_id('password').send_keys(password)
        x.find_element_by_id('password').send_keys(Keys.RETURN)   #采用回车代替点击登陆
        #print x.find_element_by_xpath('//i[contains(text(),"登录名或密码错误")]//i')
        #用Url获取的验证码是变动的，每点击一次都不同，所以这里只能采用selenium截图功能查看网页
        # imgUrl=x.find_element_by_id('check_img').get_attribute('src')
        # print imgUrl
        # session=requests.Session()
        # r=session.get(imgUrl)
        # with open('code.png','wb')as f:
        #     f.write(r.content)
        time.sleep(15)  #能截到验证码
        if x.current_url != loginUrl:
            break
        while True:
            x.save_screenshot('code.png')
            im=Image.open('code.png')
            im.show()
            im.close()
            print "如果看到提示信息【登录名或密码错误】,请按【Q】重新输入账号密码"
            code=raw_input("Code:")
            if code=="Q":
                break
            else:
                x.find_element_by_id('door').clear()
                x.find_element_by_id('door').send_keys(code)
                x.find_element_by_id('door').send_keys(Keys.RETURN)
                time.sleep(15) #等待网页加载
                print x.current_url
                if x.current_url != loginUrl:
                    break
                else:
                    print "请输入正确的验证码!!!"
            break
    print "登录成功!!!"

# 微博点赞
def dzWeibo():
    dzs=x.find_elements_by_xpath('//a[@action-type="fl_like"]/span/span/span/em[1]')
    for dz in dzs:
        try:
            dz.click()
            time.sleep(1)
        except:
            continue
    print "批量点赞成功"

#微博评论(先批量打开评论入口然后批量评论，最后批量点击发布按钮)
def plWeibo():
    review=raw_input("发表评论：")
    #批量打开评论入口
    pls=x.find_elements_by_xpath('//span[@node-type="comment_btn_text"]/span/em[1]')
    for pl in pls:
        try:
            pl.click()
            time.sleep(1)
        except:
            continue
    #批量写入评论
    texts=x.find_elements_by_xpath('//textarea[@action-type="check"]')
    for text in texts:
        try:
            text.send_keys(review.decode('utf-8'))
            time.sleep(2)
        except:
            continue
    #批量发布评论
    plbuttons=x.find_elements_by_xpath('//a[@node-type="btnText"]')
    for plbutton in plbuttons:
        try:
            time.sleep(2)
            plbutton.click()
        except:
            continue
    print "批量评论成功"

#取关全部
def qgWeibo():
    x.get("https://weibo.com/%s/follow" % uid)
    while True:
        try:
            x.find_element_by_xpath('//a[@action-type="batselect"]').click()
            i=0  #限制多选数量 ，否则出错
            for choose in x.find_elements_by_class_name("markup_choose"):
                choose.click()
                if i == 8:
                    break
                i+=1
                time.sleep(1)
            x.find_element_by_xpath('//a[@action-type="cancel_follow_all"]').click()
            x.find_element_by_xpath('//a[@class="W_btn_a btn_34px"]/span').click()
            print "已取关一部分，页面刷新中"
            time.sleep(5)
        except:
            print "取关全部已成功"
            break

#发微博
def writeWeibo():
    #x.get('https://weibo.com/u/%s/home' % uid)
    while True:
        try:
            write=raw_input("发微博(回车可取消)：")
            if write=='':
                break
            x.find_element_by_xpath('//textarea[@node-type="textEl"]').send_keys(write.decode('utf-8'))
            time.sleep(2)
            x.find_element_by_xpath('//*[@id="v6_pl_content_publishertop"]/div/div[3]/div[1]/a').click()
            print "发布成功···"
        except:
            print "错误！请重试"
            continue

#微博朋友圈
def friendsWeibo():
    print "正在进入微博朋友圈"
    x.get('https://weibo.com/friends')
    print "【1】朋友圈发动态 【2】批量点赞 【3】批量评论 【8】返回上级菜单"
    while True:
        try:
            select=raw_input("请选择(朋友圈)：")
            if int(select)==1:
                writeWeibo()
            elif int(select)==2:
                dzWeibo()
            elif int(select)==3:
                plWeibo()
            elif int(select)==8:
                break
            else:
                print "输入有误···"
                continue
        except:
            print "输入有误···"
            continue

#微博个人简单信息
def infoWeibo():
    x.get('https://weibo.com/u/%s/home' % uid)
    weiboName=x.find_element_by_xpath('//a[@class="name S_txt1"]').text
    level=x.find_element_by_xpath('//span[@node-type="levelNum"]').text
    follow=x.find_element_by_xpath('//strong[@node-type="follow"]').text
    fans=x.find_element_by_xpath('//strong[@node-type="fans"]').text
    weibo=x.find_element_by_xpath('//strong[@node-type="weibo"]').text
    print "【微博昵称：%s | 等级：%s | 关注：%s | 粉丝：%s | 微博：%s】" % (weiboName,level,follow,fans,weibo)

#主函数
loadingWeibo()
x.get('http://weibo.com/')
uid=x.current_url.split('/')[4]
print "【1】查看个人信息 【2】主页发表动态 【3】进入微博朋友圈 【4】微博取关全部 【8】退出"
while True:
    try:
        select=raw_input("请选择(主页)：")
        if int(select)==1:
            infoWeibo()
        elif int(select)==2:
            writeWeibo()
        elif int(select)==3:
            friendsWeibo()
        elif int(select)==8:
            break
        else:
            print "输入有误···"
            continue
    except:
        print "输入有误···"
        continue
