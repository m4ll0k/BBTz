#!/usr/bin/python

# m4ll0k - github.com/m4ll0k 
# favihash - Subdomains enumeration via favicon.ico hashing - (beta v.) 
# (@m4ll0k2)
'''
$ cat my_targets.txt|xargs -I %% bash -c 'echo "http://%%/favicon.ico"' > targets.txt
$ python3 favihash.py -f https://reliable-domain/favicon.ico -t targets.txt -s 

'''

from urllib import request,error,parse
import sys 
import ssl
import io
import os
import argparse
from PIL import Image 

if hasattr(ssl, '_create_unverified_context'): 
    ssl._create_default_https_context = ssl._create_unverified_context

def readfile(_):
    return [x.strip() for x in open(_,'r')]

def getHash(content1,content2):
    if hash(content1) == hash(content2):
        return True 
    return False

def getFullURL(url):
    parser_url = parse.urlsplit(url)
    if parser_url.scheme == '':
        return 'http://' + url 
    elif parser_url.scheme != '' and parser_url.scheme in ['http','https']:
        return url 
    else:
        return False

def getContent(favicon_path,is_url=True):
    content = None
    if is_url:
        try:
            content =  request.urlopen(favicon_path).read()
            return Image.open(io.BytesIO(content)).tobytes()
        except (error.HTTPError,error.URLError) as err:
            if args.show:
                print('[ i ]\033[1;31m%s\033[0m - %s'%(err,favicon_path))
    else:
        return Image.open(favicon_path).tobytes()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--favicon',help="Input favicon url or local favicon image, for compare with provided list of targets",
    action="store",required=True)
    parser.add_argument('-t','--targets',help="Provide a list of targets to compare", action="store",required=True)
    parser.add_argument('-s','--show',help="Show http errors",action="store_true",required=False,default=False)
    args = parser.parse_args()
    _bytes={
        # :)
    }['']=None
    if args.favicon:
        favicon = args.favicon
        if '://' in favicon:
            _bytes = getContent(favicon,True)
        else:
            if os.path.exists(favicon):
                _bytes = getContent(favicon,False)
            else:
                sys.exit(
                    print('[ ! ] Check your provided URL/local fivicon image')
                )
    if args.targets:
        if os.path.exists(args.targets):
            for target in readfile(args.targets):
                target_ = getFullURL(target)
                if target_ is False:
                    print('[ i ] Not supported scheme for "%s", skipped..'%target)
                    continue
                _bytes2 = getContent(target_,True)
                if getHash(_bytes,_bytes2):
                    print('[ i ]\033[1;32mSAME HASH FOUND:\033[0m \033[1;33m%s == %s\033[0m'%(args.favicon,target))
        else:
            sys.exit(
                print('[ ! ] %s not found!'%args.targets)
            )
