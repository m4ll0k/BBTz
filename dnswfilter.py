#!/usr/bin/env python3
# dnswfilter.py - dns wildcard (*) filter (detect and filter dns wildcard)
# by @m4ll0k - github.com/m4ll0k 
# Doc: https://0xpatrik.com/wildcard-domains/


import sys
if sys.version_info.major < 3:
    print('Run "%s" with python3'%sys.argv[0])
    sys.exit(0)
import os 
import argparse
# parts
try:
    from dns.resolver  import Resolver
    from dns.exception import DNSException
    from tldextract import extract 
except Exception as err:
    sys.exit(
        print(f'{err}')
    )
from multiprocessing.pool import ThreadPool
from socket import inet_aton, error 
from hashlib import sha256
from time import time

G_OUTPUT = []

# return random subdomain
def random_str():
    return sha256(str(time()).encode('utf-8')).hexdigest()

# lookup
def lookup(servers,domain):
    dns_resolver = Resolver()
    dns_resolver.nameservers = servers
    dns_resolver.lifetime = 3
    try:
        # python 3.9 query deprecation 
        if sys.version_info.minor < 9:
            answer = dns_resolver.query(domain)
        else:
            answer = dns_resolver.resolve(domain)
        return [x.to_text() for x in answer]
    except (DNSException, ValueError) as e:
        pass
    return []

# check target len and add random subdomain
def check_domain(domain):
    tld = extract(domain)
    domain_ = tld.subdomain + '.' + tld.domain
    len_domain = len(domain_)
    # check domain length
    if len_domain < 63:
        l_len = 63 - len_domain 
        random_sub = random_str()[:l_len]
        return f'{random_sub}.{domain}'
    return domain  

# read a list of targets
def readfile(path):
    return [line.strip() for line in open(path,'r')]

# check wildcard
def check_wildcard(resolvers,domain):
    f_resp = lookup(resolvers,domain)
    s_resp = lookup(resolvers,check_domain(domain))
    # sorted 
    f_resp.sort()
    s_resp.sort()
    if f_resp != s_resp and args.noWildcard:
        if args.output:
            G_OUTPUT.append(domain)
        print(f'{domain}')
    elif args.yesWildcard and f_resp == s_resp:
        if args.output:
            G_OUTPUT.append(domain)
        print(f'{domain}')

# validate ip
def valid_ip(addr):
    try:
        inet_aton(addr)
    except error:
        sys.exit(print(f'{addr} is not a valid IP address!'))
    return True

# check path
def check_path(path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return True
    else:
        sys.exit(
            print(f'Please check your list: {path}')
        )
# output 
def output_write(path,content):
    file_ = open(path,'w')
    for t in content:
        file_.write(f'{t}\n')
    file_.close()
    print(f'Output: {path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--resolvers',help="Provide a resolvers, e.g: 1.1.1.1,8.8.8.8",default="8.8.8.8",action="store")
    parser.add_argument('-l','--list',help="List of targets",default="",action="store")
    parser.add_argument('-d','--domain',help="Check single domain",default="",action="store")
    parser.add_argument('-n','--noWildcard',help="Show only domains with no wildcard, (default=True)",default=True,action="store_true")
    parser.add_argument('-y','--yesWildcard',help="Show only domains with wildcard, default=False",default=False,action="store_true")
    parser.add_argument('-o','--output',help="Output file",default="",action="store")
    parser.add_argument('-t','--threads',type=int,help="Number concurrent threads to use",default=50,action="store")
    args = parser.parse_args()
    # init 
    # resolvers list default  
    resolvers = ['8.8.8.8']
    targets   = [] 
    if args.resolvers != '8.8.8.8':
        for i in args.resolvers.split(','):
            if valid_ip(i):
                resolvers.append(i)
    if args.list != "" and args.domain == "":
        if check_path(args.list):
            targets = readfile(args.list)
    elif args.domain != "" and args.list == "":
        targets.append(args.domain)
    else:
        sys.exit(parser.print_usage())
    if args.yesWildcard:
        args.noWildcard = False
    # threads
    t_pool = ThreadPool(args.threads)
    workers = []
    for target in targets:
        w = t_pool.apply_async(
            check_wildcard,(
                resolvers, target 
            )
        )
        workers.append(w)
    for w in workers:
        w.get()
    t_pool.close()
    t_pool.join()
    if args.output:
        output_write(args.output,G_OUTPUT)
    # end 
    
