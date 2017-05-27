#!/user/bin/env python
#_*_coding:utf-8_*_
import os, re, urllib2, urllib, time, urllib, HTMLParser
import sys, json, pickle, datetime
from BeautifulSoup import BeautifulSoup
import itchat

reload(sys)
sys.setdefaultencoding('utf8')
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
url = "http://www.douban.com/group/futianzufang/discussion?start={number}"

def parseHTML():
    urlList = getAlreadyFile()
    # 登录 itchat机器人
    itchat.auto_login(enableCmdQR=-0.1, hotReload=True)
    #itchat.auto_login(hotReload=True)
    #numList = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250]
    numList = [0, 25, 50, 75, 100]
    for number in numList:
        #try:
        request = urllib2.Request(url.replace("{number}", str(number)), headers=hdr)
        page = urllib2.urlopen(request, timeout=10).read()
        #except Exception as ex:
        #    print ex
        page = page.decode('utf8').encode('utf8')
        soup = BeautifulSoup(page)
        tab = soup.findAll('table')
        trs = tab[len(tab)-1].findAll('tr')
        for tr in trs:
            tds = tr.findAll('td')
            for td in tds:
                if td.get('class') == 'title':
                    for t in td.findAll('a'):
                        title = t.get('title').encode('utf8')
                        href = t.get('href').encode('utf8')
                        msg = title + '\t' + href
                        priceList = re.findall(r"\d+", title)
                        if priceList != []:
                            for price in priceList:
                                if 1500 < int(price) < 2600:
                                    #print msg
                                    if href not in urlList:
                                        itchat.send(msg, toUserName='filehelper')
                                        # 满足条件的写入文件中，用来去重
                                        with open('./Already', 'a+') as wf:
                                            wf.write(href + '\n')
                                break

def getAlreadyFile():
    urlList = []
    with open('./Already') as rf:
        for line in rf.readlines():
            urlList.append(line.strip())
    return urlList

if __name__=='__main__':
    #getAlreadyFile()
    parseHTML()
