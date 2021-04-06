import requests
from lxml import html
import os 
import sys 

if not sys.version_info.major >= 3:
    sys.exit(print("[ ! ] Run this tool with python version 3.+"))

def usage():
    print('Usage:\n')
    print('\tpython3 {} <domain1,domain2> <cookie>'.format(sys.argv[0]))
    print('\tcat targets.txt | python3 {} <cookie>'.format(sys.argv[0]))
    print('\nby m4ll0k (@m4ll0k)\n')
    sys.exit(0)


def main(target: str, cookie:str) -> None:
    headers = {'authority': 'builtwith.com', 'cache-control': 'max-age=0', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7' }
    headers['cookie'] = cookie
    try:
        content = requests.get(f'https://builtwith.com/relationships/{target}',headers=headers).content
        html_ = html.fromstring(content)
        for target_ in html_.xpath('//td[@class="hbomb"]/a/text()'):
            print(target_)
    except Exception as err:
        sys.exit(
            print('[ ! ] ERROR: {0}'.format(
                err
            ))
        )

if len(sys.argv) > 1:
    for target in sys.argv[1].split(','):
        try:
            main(target,sys.argv[2])
        except Exception as err:
            usage()
else:
    for target in sys.stdin.readlines():
        t = target.strip()
        if target == '\n':
            usage()
        try:
            main(t,sys.argv[1])
        except Exception as err:
            usage()
