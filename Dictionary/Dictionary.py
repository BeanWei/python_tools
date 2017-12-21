# -*- coding: utf-8 -*-
# bulid by Bean_Wei/ 2017/11/14 14:15

import urllib
import urllib2
import json
import time
import hashlib
import tkMessageBox
from Tkinter import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def Translate():
    queryText=entry.get()
    url ='https://openapi.youdao.com/api/'
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    appKey = '686e8974bd7e8080'
    appSecret = 'qWe67kgyclnHQH9N5XnYFqBu4VLyr8Se'
    langFrom ='auto'
    langTo ='auto'
    salt = str(int(round(time.time() * 1000)))
    sign_str = appKey + queryText + salt +appSecret
    sign = hashlib.md5(sign_str).hexdigest()
    payload = {
        'q': queryText,
        'from':langFrom,
        'to':langTo,
        'appKey':appKey,
        'salt':salt,
        'sign':sign
    }
    info = urllib.urlencode(payload)
    target_url =url +'?' +info
    request = urllib2.Request(target_url, headers=header)
    response = urllib2.urlopen(request)
    data=json.loads(response.read())
    translationResult = data['translation']
    if isinstance(translationResult, list):
        translationResult = translationResult[0]
        label.config(text=translationResult)
    if "basic" in data:
        youdaoResult = "\n".join(data['basic']['explains'])
        label.config(text=translationResult+'\n'+youdaoResult)

def ask_quit():
    if tkMessageBox.askyesno('Tip','Exit?'):
        window.quit()

window=Tk()
window.protocol('WM_DELETE_WINDOW',ask_quit)
window.title('*詞-典*=@Author:Bean_Wei')
photo=PhotoImage(file='Pic.gif')
window.geometry('702x405')
window.resizable(width=False, height=False)
entry=Entry(window,text="0",width=405,bg='#B2BCC5',font = ('Helvetica', '14', 'bold'))
entry.pack()
Button(window,text='翻译(其他 *译* 中文 *译* 英)',width=405,height=2,command=Translate,bg='#B2BCC5',font=("Arial, 16")).pack()
label=Label(window,text='@Author:Bean_Wei',height=405,image=photo,compound='center',font = ("Arial, 16"))
label.pack()
window.mainloop()