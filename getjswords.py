# by m4ll0k - github.com/m4ll0k 
# (@m4ll0k2)

import requests 
from jsbeautifier import beautify
import sys,re
import string 

blacklisted = [
"await"
"break"
"case"
"catch"
"class"
"const"
"continue"
"debugger"
"default"
"delete"
"do"
"else"
"enum"
"export"
"extends"
"false"
"finally"
"for"
"function"
"if"
"implements"
"import"
"in"
"instanceof"
"interface"
"let"
"new"
"null"
"package"
"private"
"protected"
"public"
"return"
"super"
"switch"
"static"
"this"
"throw"
"try"
"True"
"typeof"
"var"
"void"
"while"
"with"
"abstract"
"else"
"instanceof"
"super"
"boolean"
"enum"
"int"
"switch"
"break"
"export"
"interface"
"synchronized"
"byte"
"extends"
"let"
"this"
"case"
"false"
"long"
"throw"
"catch"
"final"
"native"
"throws"
"char"
"finally"
"new"
"transient"
"class"
"float"
"null"
"true"
"const"
"for"
"package"
"try"
"continue"
"function"
"private"
"typeof"
"debugger"
"goto"
"protected"
"var"
"default"
"if"
"public"
"void"
"delete"
"implements"
"return"
"volatile"
"do"
"import"
"short"
"while"
"double"
"in"
"static"
"with"
"alert"
"frames"
"outerHeight"
"all"
"frameRate"
"outerWidth"
"anchor"
"function"
"packages"
"anchors"
"getClass"
"pageXOffset"
"area"
"hasOwnProperty"
"pageYOffset"
"Array"
"hidden"
"parent"
"assign"
"history"
"parseFloat"
"blur"
"image"
"parseInt"
"button"
"images"
"password"
"checkbox"
"Infinity"
"pkcs11"
"clearInterval"
"isFinite"
"plugin"
"clearTimeout"
"isNaN"
"prompt"
"clientInformation"
"isPrototypeOf"
"propertyIsEnum"
"close"
"java"
"prototype"
"closed"
"JavaArray"
"radio"
"confirm"
"JavaClass"
"reset"
"constructor"
"JavaObject"
"screenX"
"crypto"
"JavaPackage"
"screenY"
"Date"
"innerHeight"
"scroll"
"decodeURI"
"innerWidth"
"secure"
"decodeURIComponent"
"layer"
"select"
"defaultStatus"
"layers"
"self"
"document"
"length"
"setInterval"
"element"
"link"
"setTimeout"
"elements"
"location"
"status"
"embed"
"Math"
"String"
"embeds"
"mimeTypes"
"submit"
"encodeURI"
"name"
"taint"
"encodeURIComponent"
"NaN"
"text"
"escape"
"navigate"
"textarea"
"eval"
"navigator"
"top"
"event"
"Number"
"toString"
"fileUpload"
"Object"
"undefined"
"focus"
"offscreenBuffering"
"unescape"
"form"
"open"
"untaint"
"forms"
"opener"
"valueOf"
"frame"
"option"
"window"
"yield"
]

def getWords(content:str):
    allWords = []
    content = beautify(content)
    regex_content = re.findall('[a-zA-Z0-9_\-\.]+',content)
    for word in regex_content:
        if '.' in word:
            w = word.split('.')[-1:][0]
            if w and w not in allWords:
                allWords.append(w)
        elif len(word) == 1:
            if word in string.punctuation:
                pass 
            elif word in string.ascii_letters:
                if word not in allWords:
                    allWords.append(word)
            elif word in string.digits:
                pass
        else:
            if word not in allWords:
                allWords.append(word) 
    _allWords = allWords
    allWords = []
    for word in _allWords:
        if word not in blacklisted:
            if word not in allWords:
                allWords.append(word)
    return allWords

def main(jsFile):
    bad = not 1
    if '://' not in jsFile or '.js' not in jsFile:
        print('Bad URL: %s'%jsFile,end="")
        print(', please check your url',end="")
        print(', pass..')
        bad = not 0 
    if bad is False:
        try:
            req = requests.get(jsFile)
            content = req.content.decode('utf-8','replace')
            words = getWords(content)
            for word in words:
                print(word)
        except Exception as err:
            sys.exit(print(err))


def usage():
    name = sys.argv[0]
    print('Usage:')
    print('\tpython3 %s https://example.com/javascripts/main.js'%name)
    print('\tcat my_js_files.txt | python3 %s'%name)
    print('by @m4ll0k - github.com/m4ll0k')
    sys.exit(0)

if len(sys.argv) == 2:
    main(
        sys.argv[1]
    )
else:
    for jsFile in sys.stdin.readlines():
        jsFile = jsFile.strip()
        if jsFile == '\n':
            usage()
        main(jsFile)