#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# coded by m4ll0k (@m4ll0k2) github.com/m4ll0k
# -------------------------------------------
'''
- Don't use this tool because your ip will be blocked by Shodan!

Get ports,vulnerabilities,informations,banners,..etc for any IP with Shodan (no apikey! no rate limit!)


'''


''' **** USAGE **** 
# python3 shodanfy.py <ip> [OPTIONS] 
e.g:
    python3 shodanfy.py 111.111.111.111 
    python3 shodanfy.py 111.111.111.111 --getports
    python3 shodanfy.py 111.111.111.111 --getvuln
    python3 shodanfy.py 111.111.111.111 --getinfo
    python3 shodanfy.py 111.111.111.111 --getmoreinfo
    python3 shodanfy.py 111.111.111.111 --getbanner
    python3 shodanfy.py 111.111.111.111 --getports --getvuln
    python3 shodanfy.py 111.111.111.111 --getports --proxy 127.0.0.1:8080
# support pipeline the --stdin option is required for pipeline..
# echo "<ip>" or cat ips.txt | python3 shodanfy.py --stdin [OPTIONS]
e.g:
    echo "111.111.111.111"|python3 shodanfy.py --stdin 
    echo "111.111.111.111"|python3 shodanfy.py --stdin --getvuln 
    cat ips.txt|python3 shodanfy.py --stdin --getports
'''

import requests 
from lxml import html 
import sys
import re

def getContentFromShodan(ip:str,proxy:str)->str:
    try:
        if "ipinfo" in proxy:
            return requests.get(
                '{}'.format(ip),
                headers = {
                    'User-Agent' : 'Mozilla/5.0'
                },
                proxies = {
                    'http' : proxy,
                    'https' : proxy,
                }
            )
        return requests.get(
            'https://www.shodan.io/host/{}'.format(ip),
            headers = {
                'User-Agent' : 'Mozilla/5.0'
            },
            proxies = {
                'http' : proxy,
                'https' : proxy,
            }
        )
    except Exception as e:
        sys.exit(
            print(e)
        )

def main(args:dict) -> None:
    ip = args.get('ip')
    v = {}
    d = []
    proxy = args.get('proxy')
    socks5 = args.get('socks5')
    if socks5 != "":
        proxy = "socks5://{}".format(socks5)
    getports = False if args.get('getports') == False else True
    getinfo = False if args.get('getinfo') == False else True
    getvuln = False if args.get('getvulns') == False else True
    getmoreinfo = False if args.get('getmoreinfo') == False else True
    getbanner = False if args.get('getbanner') == False else True
    getall = True
    if any([getports,getinfo,getvuln,getmoreinfo,getbanner]):
        getall = False
    else:
        getports=getinfo=getvuln=getmoreinfo=getbanner=True
    # --- 
    r = getContentFromShodan(ip,proxy=proxy)
    #r2 = getContentFromShodan('http://ipinfo.io',proxy=proxy)
    # --
    print("[*] YOUR IP: " + ip)
    if r.status_code == 200:
        tree = html.fromstring(r.content)
        if tree.xpath('//ul[@class="ports"]/li/a/text()') != []:
            if getports:
                print('[+] Get ports.. ')
                for p in tree.xpath('//ul[@class="ports"]/li/a/text()'):
                    print('\t'+p)
        if tree.xpath('//table[@class="table"]/tbody/tr/td/text()') != []:
            co = tree.xpath('//table[@class="table"]/tbody/tr/td/text()')
            ro = tree.xpath('//table[@class="table"]/tbody/tr/th/text()')
            di = dict(zip(co,ro))
            if getinfo:
                print('[+] Get info...')
            for i in di.items():
                if 'CVE-' in str(i[1]):
                    v[i[1]] = i[0]
                else:
                    if getinfo:
                        print('\t'+i[0]+' -> '+i[1])
        if v != {}:
            if getvuln:
                print('[+] Get vulns...')
                print('-'*40)
                c = ['CVE','Description']
                cves = []
                for i in v.items():
                    print('CVE: '+i[0])
                    print('Description:\n'+i[1])
                    print('-'*40)
        if tree.xpath('//ul[@class="services"]//div[@class="service-details"]'):
            title = []
            banner = []
            port = tree.xpath('//ul[@class="services"]//div[@class="service-details"]//div[@class="port"]/text()')
            proto = tree.xpath('//ul[@class="services"]//div[@class="service-details"]//div[@class="protocol"]/text()')
            state = tree.xpath('//ul[@class="services"]//div[@class="service-details"]//div[@class="state"]/text()')
            if tree.xpath('//ul[@class="services"]//div[@class="service-main"]'):
                title=tree.xpath('//ul[@class="services"]//div[@class="service-main"]/h3/text()')
                if tree.xpath('//ul[@class="services"]//div[@class="service-main"]/h3/small'):
                    versions = tree.xpath('//ul[@class="services"]//div[@class="service-main"]/h3/small/text()')
                if tree.xpath('//ul[@class="services"]//div[@class="service-main"]/pre'):
                    banner=tree.xpath('//ul[@class="services"]//div[@class="service-main"]/pre/text()')
            for i in range(len(port)):
                po = port[i] 
                pr = proto[i]
                st = state[i]
                try:
                    vv = versions[i]
                except:
                    vv = "None"
                try: 
                    tt = title[i]
                except:
                    tt = "None"
                bb = banner[i]
                d.append((po,pr,st,tt,vv,bb))
            # proto 
            if getbanner or getmoreinfo:
                if getbanner:
                    print('[+] Get banner..')
                else:
                    print('[+] Get moreinfo..')
                for i in d:
                    if getmoreinfo:
                        print('\nPort: %s/%s\t%s\t%s (%s) '%(i[0],i[1],i[2],i[3],i[4]))
                    if getbanner:
                        print('Banner:\n%s'%i[5])
    else:
        print('Not information found for this ip..')

args = {
    'getports': False,
    'getbanner': False, 
    'getvulns': False,
    'getinfo': False,
    'getmoreinfo': False,
    'getall': True,
    'ip':  "",
    'stdin':False,
    'proxy': "",
    'socks5': ""
}

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Usage: python3 shodanfy.py <ip> [OPTIONS]\n')
        print('\t--stdin\t\tGet ips from stdin (required)')
        print('\t--proxy\t\tSet proxy (host:port)')
        print('\t--socks5\t\tSet proxy socks5 (host:port)')
        print('\t--getall\tGet all informations,vulns,.. (Default)')
        print('\t--getvuln\tGet vulnerabilities for this ip (CVEs)')
        print('\t--getinfo\tGet basic info (hostname,ports,country..)')
        print('\t--getmoreinfo\tGet more info (port,protocol,state,version..)')
        print('\t--getports\tGet all ip ports..')
        print('\nCoded by @m4ll0k (github.com/m4ll0k)\n')
        sys.exit(0)
    for arg in sys.argv:
        if arg == '--getvuln':
            args['getvulns'] = True
        if arg == '--getinfo':
            args['getinfo'] = True 
        if arg == '--getbanner':
            args['getbanner'] = True 
        if arg == '--getmoreinfo':
            args['getmoreinfo'] = True 
        if arg == '--proxy':
            proxy = sys.argv[sys.argv.index('--proxy') + 1]
            if '--' in proxy:
                sys.exit(print(
                    'Please check your proxy, (host:port)'
                ))
            args.update({"proxy":str(proxy)})
        if arg == '--socks5':
            socks5 = sys.argv[sys.argv.index('--socks5') + 1]
            if '--' in socks5:
                sys.exit(print(
                    'Please check your proxy socks5, (host:port)'
                ))
            args.update({"socks5":str(socks5)})
        if arg == '--getports':
            args['getports'] = True
        if arg == '--stdin':
            args['stdin'] = True
        if re.search(r'\d+.\d+.\d+.\d+',arg):
            args['ip'] = re.search(r'\d+.\d+.\d+.\d+',arg).group(0)
            # ip checker
            for i in args['ip'].split('.'):
                if int(i) > 255:
                    sys.exit(print('Wrong ip!'))
            if len(args['ip'].split('.')) != 4:
                sys.exit(print("Wrong ip!!!"))
    if args['ip'] == "" and args['stdin'] == False:
        sys.exit(print('Wrong ip or ip not specified!!'))
    else:
        if args['stdin']:
            for i in sys.stdin.readlines():
                i = i.strip()
                if i != "":
                    print('[+] IP: %s'%i)
                    if re.search(r'[\d{3}\.]{4,15}',i):
                        args['ip'] = re.search(r'[\d{3}\.]{4,15}',i).group(0)
                    if args['ip'] == "":
                        sys.exit(print('Wrong ip or ip not specified!!'))
                    main(args)
        elif args['stdin'] is False:
            print("[+] IP: %s"%args['ip'])
            main(args)
        
