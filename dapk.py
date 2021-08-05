#!/usr/bin/env pytho
# by @m4ll0k 
# 
# dapk.py - download all apk versions of an org from apkmirror.com

# usage
'''
E.g: Downlad all paypal apk

$ python3 dapk.py "paypal" "paypal-apk"

Without threads so it will be slow, however this is just an example, you can improve this tool

'''


import requests 
import os 
import re
import random 
import sys 
try:
    import requests 
    from lxml.html import fromstring as FS
    from random_user_agent.user_agent import UserAgent
    from random_user_agent.params import SoftwareName, OperatingSystem
except Exception as err:
    sys.exit(print(f'{err}'))



'''{UserAgent(
        software_names=['chrome','safari'],
        operating_systems=['mac'],
        limit=50
    ).get_random_user_agent()}'''

HEADERS = lambda : {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
}

LIST_OF_PK = [
# (url,package_name)
]
APKM_URL = 'https://www.apkmirror.com'


if len(sys.argv) <= 2:
    sys.exit(print(f'\npython3 {sys.argv[0]} <name-of-packages> <output-dir>\n'))

NAME_PK = sys.argv[1] 
DIRECTORY =  sys.argv[2]

if os.path.exists(DIRECTORY):
    if os.path.isdir(DIRECTORY) is True:
        pass 
    else:
        sys.exit(print('[ ! ] Check your directory output!'))
else:
    os.mkdir(DIRECTORY)

def download_apk(url,pkname):
    print(f'[ + ] Download.. {pkname} -> {os.path.abspath(DIRECTORY+"/"+pkname)}')
    r = requests.get(url,stream=True,headers=HEADERS())
    open(f'{DIRECTORY}/{pkname}','wb').write(r.content)


def get_pages_len():
    l = []
    for i in range(1,50):
        r = requests.get(f'https://www.apkmirror.com/uploads/page/{i}/?q={NAME_PK}',headers=HEADERS(),allow_redirects=True)
        if '<p>No uploads found</p>' in r.content.decode('utf-8'):
            break
        if i == 1:
            l.append(r.url)
        for href in FS(r.content or "").xpath('//a[@class="page larger"]/@href'):
            href = APKM_URL + href
            if href not in l:
                l.append(href)
    return l 


def get_all_info(url):
    r = requests.get(url,headers=HEADERS())
    for href in FS(r.content).xpath('//div[@class="iconsBox "]/div[@class="downloadIconPositioning"]/a/@href'):
        href = APKM_URL + href
        ADD = (href,href.split('/')[-2] + '.apk')
        if ADD not in LIST_OF_PK:
            LIST_OF_PK.append(
                ADD 
            )

def getDowloadUrl(content):
    for i in FS(content).xpath('//@href'):
        if 'download.php' in i:
            return APKM_URL + i 
    return 


def get_apk_only(url,pkname):
    r = requests.get(url,headers=HEADERS())
    ally = FS(r.content).xpath('//div[@class="table topmargin variants-table"]/*')
    if type(ally) is list and ally != []:
        ally.pop(0)
    for dom in ally:
        if '\nBUNDLEAPK' in dom.text_content():
            pass
        elif '\nAPK' in dom.text_content():
            for i in list(set(dom.xpath('div[@class="table-cell rowheight addseparator expand pad dowrap"]/a/@href'))):
                href = APKM_URL + i +'download/?forcebaseapk'
                r = requests.get(href,headers=HEADERS())
                url = getDowloadUrl(r.content)             
                if url not in [None,'None','none']:
                    download_apk(url,pkname)


def main():
    lens = get_pages_len()
    
    if lens == []:
        sys.exit(print(f'[ ! ] {NAME_PK} not found! Check here https://www.apkmirror.com/uploads/?q={NAME_PK}'))

    print(f'[ + ] Found {len(lens)} pages..')
    
    for url in lens:
        get_all_info(url)

    print(f'[ + ] Found {len(LIST_OF_PK)} releases..')

    for t in LIST_OF_PK:
        get_apk_only(t[0],t[1])

main()
