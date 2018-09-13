#!/usr/bin/env python
# encoding: utf-8

'''

@author: liyuhang

@license: (C) Copyright 2013-2017,beijing SQD.

@contact: liyuhang@cryo-service.com

@software: garner

@file: iqiyi.py.py

@time: 2018/9/11 18:32

@desc:
'''


import requests
import codecs
import threading
import sys
import os


BASE_URL = 'https://jx.618g.com'
DOWNLOAD_URL = ''

f = codecs.open('save.txt', 'w+', 'utf-8')
START_STR = "/m3u8.php?url="
END_STR = '"'

def openUrl(url):
    header = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    cookie = {
        'FSKS_Sign' : '66844B5AACD8BBE040BA2DBA409ACDF4788B578E3617E13ED1F6BE0A6656528B2D2EA196A6B5C8CF',
        'UM_distinctid' : '163aa4d7efd1b6-024059989125e6-3961430f-144000-163aa4d7efebd',
        'FSKS_Token' : 'd2VWanlSeHc5QkpGU09oYmo5SWlZRFZKX1BuOU1DazNBanE3YlhMVGdnVnI4WFZJaFNHdFFFVHF4MGZ0Qm1hajBQRTg1SktDdjFvUGIyeG9SVm42Qk42WGhhUlgyNm51TDFpb2wyeWI3RU0vUkp4MXluTFdmQlk',
        'CNZZDATA1260594368' : '502073154-1527568985-null%7C1536667603',
        'yd_srvbl' : '5d51bbe56ef265559d3a07a545d0a59c'
     }
    s = requests.session()
    requests.utils.add_dict_to_cookiejar(s.cookies, cookie)

    dat = {'url':url}

    re = requests.get(BASE_URL, headers = header, params = dat)
    webText = re.text
    if webText:
        pos = webText.find(START_STR)
        if pos >= 0:
            pos = pos + len(START_STR)
            pos2 = pos + webText[pos:].find(END_STR)
            if pos2 > 0:
                DOWNLOAD_URL = webText[pos:pos2]
                return DOWNLOAD_URL
    return ''

def getM3U8(url):
    if url == '':
        return ''
    re = requests.get(url)
    if re.text:
        return re.content.decode()
    return ''

def getReadM3U8(url, text):
    if url == '':
        return ''

    if text == '':
        return ''

    M3U8_REAL = 'index.m3u8'
    for line in str.split(text, '\n'):
        if line.find(M3U8_REAL) > 0:
            s = str.split(url, '/')
            s[-1] = line
            url = '/'.join(s)
            return url
    return ''

downloadUrl = ''
dosnloadNames = []
def downloadTs(name):
    if name.find('.ts') > 0:
        re = requests.get(downloadUrl+'/'+name)
        with open(name, 'wb') as mp4File:
            print(name)
            mp4File.write(re.content)

def addMp4(names):
    mp4File = open('a.mp4', 'ab')
    print("合并mp4文件:\r\n")
    for name in names:
        if name.find('.ts') > 0:
            print(name)
            with open(name, 'rb') as tsFile:
                mp4File.write(tsFile.read())
            os.remove(name)
    mp4File.close()


if "__main__" == __name__:
    mp4Url = 'http://www.le.com/ptv/vplay/2057327.html?ref=ym0210'

    if len(sys.argv) > 1:
        mp4Url = sys.argv[1]



    tmpUrl = openUrl(mp4Url)
    text = getM3U8(tmpUrl)
    ret = getReadM3U8(tmpUrl, text)
    print(ret)
    re = requests.get(ret)
    if re.text:
        dosnloadNames = re.content.decode().split('\n')
        f.write(re.content.decode())

        downloadUrl = '/'.join(ret.split('/')[0:-1])


    threads = []
    for i in dosnloadNames:
        t = threading.Thread(target=downloadTs, args=(i,))
        threads.append(t)
    for t in threads:
        t.start()
        while True:
            if len(threading.enumerate()) < 20:
                break

    addMp4(dosnloadNames)