# saml decoder #

import os,sys
import zlib
import base64
import html
from urllib import parse
import xml.dom.minidom


data = sys.argv[1]

data = parse.unquote(html.unescape(data))

deflate = base64.b64decode(data)

data = zlib.decompress(deflate,-zlib.MAX_WBITS)

if '--pretty' in sys.argv[1:]:
	print(f'\n{xml.dom.minidom.parseString(data).toprettyxml()}\n')
else:
	print(f'\n{data.decode("utf-8")}\n')
