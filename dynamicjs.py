#!/usr/bin/python

#  by m4ll0k (@m4ll0k2)
#  github.com/m4ll0k


import requests
import sys
import argparse

def Process(url:str)-> None:
    headers = {} 
    if args.headers != "":
        for header in args.headers.split(','):
            h = header.split(':')
            headers[h[0]] = h[1]
    if args.cookies != "":
        headers['Cookie'] = args.cookies
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    try:
        req1 = requests.get(
            url = url,
            headers = headers
        )
        req2 = requests.get(
            url = url,
            headers = headers
        )
        if req1.status_code == req2.status_code:
            if req1.content != req2.content:
                print('[ + ] Dynamic js file: %s with %s status code'%(req1.url,req1.status_code))
    except Exception as err:
        print('[ E ] %s'%err)

def main():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',help="input js file, e.g: target1/main.js,target1/main2.js,..",action="store",default="")
    parser.add_argument('-s','--stdin',help="get stdin input",action="store_true",default=False)
    parser.add_argument('-c','--cookies',help="set cookie",action="store",default="")
    parser.add_argument('-H','--headers',help="set headers, e.g: \"name:value;name:value\"",action="store",default="")
    args = parser.parse_args()
    if args.input == "" and args.stdin is False:
        sys.exit(
            print('[ + ] python3 %s -h'%sys.argv[0])
        )
    else:
        targets = []
        if args.input and args.stdin is False:
            targets.extend(args.input.split(','))
        elif args.stdin is True:
            for target in sys.stdin.readlines():
                target = target.strip()
                if target == '\n':
                    sys.exit(
                        print('[ + ] python3 %s -h'%sys.argv[0])
                    )
                else:
                    targets.append(target)
        for target in targets:
            print('[ + ] URL: %s'%target)
            Process(target)
            




    
