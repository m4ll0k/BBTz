# by m4ll0k - github.com/m4ll0k
# google-ct-exposer.py - Discover sub-domains by searching through Certificate Transparency logs
# twitter @m4ll0k

'''
GCTExposer - Discover sub-domains by searching through Certificate Transparency logs using Google Transparencyreport
'''


import requests 
import json 
import argparse

def contentParser(content:str):
    content = json.loads(content.decode('utf-8').replace('\n','').replace(')]}\'',''))
    next_ = content[0][3]
    domains = content[0][1]
    return domains,next_

def getContent(domain):
    try:
        req = requests.get('https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?include_subdomains=true&domain={domain}'.format(
            domain=domain
        ))
        return req
    except Exception as _errors:
        print('[ ERROR ] {_errors}'.format(_errors=_errors))

def getNextContent(page):
    try:
        req = requests.get('https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch/page?p={page}'.format(
            page=page
        ))
        return req.content
    except Exception as _errors:
        print('[ ERROR ] {_errors}'.format(_errors=_errors))

def GCTExposer(domain,more):
    domains,next_ = contentParser(getContent(domain).content)
    for i in domains:
        if args.moreinfo:
            print("{_} -> {__}".format(_=i[1],__=i[2]))
        else:
            print(i[1])
    range_ = next_[-1]
    for i in range(range_ - 1):
        domains,next_= contentParser(getNextContent(next_[1]))
        next_ = next_ 
        for ii in domains:
            if args.moreinfo:
                print("{_} -> {__}".format(_=ii[1],__=ii[2]))
            else:
                print(ii[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--moreinfo',help="Show more crt informations",required=False,default=False,action="store_true")
    parser.add_argument('-d','--domain',required=True,default="",help="Target, e.g: uber.com",action="store")
    args = parser.parse_args()
    if args.domain == "":
        sys.exit(parser.print_help())
    GCTExposer(args.domain,args.moreinfo)

    
