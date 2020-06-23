
import requests
from lxml import html
import os 
import sys 

if not sys.version_info.major >= 3:
    sys.exit(print("[ ! ] Run this tool with python version 3.+"))

def usage():
    print('Usage:\n')
    print('\tpython3 {} domain1,domain2,domain3,..'.format(sys.argv[0]))
    print('\tcat targets.txt | python3 {} '.format(sys.argv[0]))
    print('\nby m4ll0k (@m4ll0k2)\n')
    sys.exit(0)


def main(target: str) -> None:
    try:
        content = requests.get('https://builtwith.com/relationships/{0}'.format(target)).content
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
        main(target)
else:
    for target in sys.stdin.readlines():
        t = target.strip()
        if target == '\n':
            usage()
        main(t)

