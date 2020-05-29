# by m4ll0k 
# github.com/m4ll0k

import sys
try:
    import jsbeautifier
    import requests
except Exception as e:
    sys.exit(print("{0}.. please download this module/s".format(e)))

def beauty(content:str)->str:
    return jsbeautifier.beautify(content.decode())

def getjs(url:str)->dict:
    try: return requests.get(url) 
    except: return {'content':None}

def main()->None:
    try:
        url = sys.argv[1]
        output = sys.argv[2]
    except:
        sys.exit(print("\nUsage:\tpython3 {0} <url> <output>\n".format(sys.argv[0])))
    if '.js' in url:
        r = getjs(url)
        if r.status_code == 200:
            js = beauty(r.content)
            if output:
                _file = open(sys.argv[2],"w")
                _file.write(js)
                _file.close()
                print("Done! file saved here -> \"{0}\"".format(_file.name))
    else:
        sys.exit(print("\".js\" not found in URL ({}).. check your url".format(sys.argv[1])))

main()