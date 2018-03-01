# -*- coding: utf-8 -*-
# bulid by Bean_Wei/ 2018/2/3 8:50

'''
转灰度公式
    大部分图像处理系统使用的公式
        #Y' =  0.2126 R' + 0.7152 G' + 0.0722 B'
    如果是线性空间，则用下面这个公式
        #Y' =  0.299 R' + 0.587 G' + 0.114 B'
'''


from PIL import Image
codeLib = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''#生成字符画所需的字符集
count = len(codeLib)

def transform1(image_file):
    image_file = image_file.convert("L")#转换为黑白图片，参数"L"表示黑白模式
    codePic = ''
    for h in range(0,image_file.size[1]):  #size属性表示图片的分辨率，'0'为横向大小，'1'为纵向
        for w in range(0,image_file.size[0]):
            gray = image_file.getpixel((w,h)) #返回指定位置的像素，如果所打开的图像是多层次的图片，那这个方法就返回一个元组
            codePic = codePic + codeLib[int(((count-1)*gray)/256)]#建立灰度与字符集的映射
        codePic = codePic+'\r\n'
    return codePic

def transform2(image_file):
    codePic = ''
    for h in range(0,image_file.size[1]):
        for w in range(0,image_file.size[0]):
            g,r,b = image_file.getpixel((w,h))
            gray = int(r* 0.299+g* 0.587+b* 0.114)    #图片没有转灰度的话得求出灰度值，r* 0.299+g* 0.587+b* 0.114即为求灰度值公式
            codePic = codePic + codeLib[int(((count-1)*gray)/256)]
        codePic = codePic+'\r\n'
    return codePic


fp = open(u'timg.jpg','rb')
image_file = Image.open(fp)
image_file=image_file.resize((int(image_file.size[0]*0.35), int(image_file.size[1]*0.15)))#调整图片大小
print u'Info:',image_file.size[0],' ',image_file.size[1],' ',count

tmp = open('output.txt','w')
tmp.write(transform1(image_file))
tmp1.close()
tmp.close()



