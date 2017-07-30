#!/usr/bin/python3

from bs4 import BeautifulSoup
from crawler.utils import urltool

def encode_fix(text):
    return text.replace('\u3000', '')

def remove_linefeed(text):
    return text.replace('\n', '')

class MovieObj:
    def __init__(self):
        self.link = ''

    def setlink(self, link):
        self.link = link

    def setattr(self, text):
        if urltool.start_with(text, '译名'):
            self.name_tr = text[2:].strip()
        elif urltool.start_with(text, '片名'):
            self.name = text[2:].strip()
        elif urltool.start_with(text, '年代'):
            self.year = text[2:].strip()
        elif urltool.start_with(text, '产地') or urltool.start_with(text, '国家') or urltool.start_with(text, '地区'):
            self.country = text[2:].strip()
        elif urltool.start_with(text, '类别') or urltool.start_with(text, '类型'):
            self.type = text[2:].strip()
        elif urltool.start_with(text, '语言'):
            self.language = text[2:].strip()
        elif urltool.start_with(text, '字幕'):
            self.subtitles = text[2:].strip()
        elif urltool.start_with(text, '上映日期'):
            self.releasedate = text[4:].strip()
        elif urltool.start_with(text, 'IMDb评分'):
            self.imdb = text[6:].strip()
        elif urltool.start_with(text, '片长'):
            self.length = text[2:].strip()
        elif urltool.start_with(text, '导演'):
            self.director = text[2:].strip()
        elif urltool.start_with(text, '主演'):
            self.actor = text[2:].strip()
        elif urltool.start_with(text, '简介'):
            text.replace('【下载地址】', '')
            self.description = text[2:].strip()

    def __str__(self):
        return self.name + '[' + self.year + '/' + self.country + ']:' + self.type

def html_analyse(text):
    mo = MovieObj()

    bs = BeautifulSoup(text, 'lxml')
    mo.setlink(bs.div.find(id='Zoom').a['href'])
    
    bs.div.find(id='Zoom').table.clear()
    #print(bs.div.find(id='Zoom').text)

    fix_text = remove_linefeed(encode_fix(bs.div.find(id='Zoom').text))
    msglist = fix_text.split('◎')
    #print(msglist)
    for msg in msglist:
        mo.setattr(msg)
    print(mo)

if __name__ == '__main__':
    html_analyse(open('ghost.html'))
