import base64,time
from urllib import request
import requests,re
from bs4 import BeautifulSoup
from prettytable import PrettyTable

PAGE_NUM = 1

#定义数据包头部
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

#shadowsocks支持的加密方式
encodway = [
    'rc4-md5',
    'salsa20',
    'chacha20',
    'aes-256-cfb',
    'aes-192-cfb',
    'aes-128-cfb',
    'aes-256-ctr',
    'aes-192-ctr',
    'aes-128-ctr',
    'bf-cfb',
    'camellia-128-cfb',
    'camellia-192-cfb',
    'camellia-256-cfb',
    'aes-128-gcm',
    'aes-192-gcm',
    'aes-256-gcm',
    'chacha20-ietf-poly1305',
    'xchacha20-ietf-poly1305',
            ]

encodway2 = [
    'chacha20-ietf-poly1305'
]

#通过正则匹配shadowsocks链接
def get_ssAddr(html):
    tar = 'ss://.*?</div>'
    target = re.findall(tar,html)
    if target:
        ssAddr = target[0]
        return ssAddr

def get_detailAddr(html):
    tar = 'href=.*?target="_blank'
    target = re.findall(tar, html)
    if target:
        detailAddr = target
        return detailAddr
    else:
        return 'null'

table = PrettyTable(['title','abstract','link','content'])
for x in encodway2:
    # 将str转换成byte才能进行base64编码，然后再转换回str才能进行字符串处理
    query = str(base64.b64encode(x.encode(encoding='utf-8')),encoding='utf8').strip('=')
    for k in range(0,PAGE_NUM):
        try:
            url = 'http://www.baidu.com/s?wd=%s&pn=%i' % (query, k+1)
            try:
                req = request.Request(url, None, headers)
                resp = request.urlopen(req)
                html = str(resp.read(), 'utf-8')
                ssAddr = get_ssAddr(html)
                detailAddr = get_detailAddr(html)
                print(ssAddr)
            except Exception as e:
                print(e)
                exit(0)


        except Exception as e:
            print(e)
