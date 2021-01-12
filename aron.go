/*
** -----------------------------------
** Aron - Hidden Parameters Bruteforce 
** https://github.com/m4ll0k
** -----------------------------------
*/

package main
import (
        "os"
		"fmt"
		"flag"
		"time"
		"bufio"
		"bytes"
		"strings"
		"net/http"
		"io/ioutil"
)

var BLACK   = "\033[1;30m"  // black
var LBLACK  = "\033[0;30m"  // light black
var RED     = "\033[1;31m" 
var LRED    = "\033[0;31m" 
var GREEN   = "\033[1;32m"
var LGREEN  = "\033[0;32m"
var YELLOW  = "\033[1;33m"
var LYELLOW = "\033[0;33m"
var BLUE    = "\033[1;34m"
var LBLUE   = "\033[0;34m"
var PURPLE  = "\033[1;35m"
var LPURPLE = "\033[0;35m"
var CYAN    = "\033[1;36m"
var LCYAN   = "\033[0;36m"
var GRAY    = "\033[1;37m"
var LGRAY   = "\033[0;37m"
var WHITE   = "\033[1;38m"
var LWHITE  = "\033[0;38m"
var RESET   = "\033[0m"
// labels
var INFO = "[i]"
var PLUS = "[+]"
var LESS = "[-]"
var TEST = "[*]"
var WARN = "[!]"
var ASK  = "[?]"

func Info(str string,color bool) {
	if color{
		fmt.Printf("%s%s%s %s%s%s\n",YELLOW,INFO,RESET,YELLOW,str,RESET)
	} else{
		fmt.Printf("%s%s%s %s\n",YELLOW,INFO,RESET,str)
	}
}
//
func Plus(str string,color bool) {
	if color{
		fmt.Printf("%s%s%s %s%s%s\n",GREEN,PLUS,RESET,GREEN,str,RESET)
	} else{
		fmt.Printf("%s%s%s %s\n",GREEN,PLUS,RESET,str)
	}
}
//
func Less(str string,color bool) {
	if color{
		fmt.Printf("%s%s%s %s%s%s\n",LRED,LESS,RESET,LRED,str,RESET)
	} else{
		fmt.Printf("%s%s%s %s\n",LRED,LESS,RESET,str)
	}
}
//
func Test(str string,color bool) {
	if color{
		fmt.Printf("%s%s%s %s%s%s\n",BLUE,TEST,RESET,BLUE,str,RESET)
	} else{
		fmt.Printf("%s%s%s %s\n",BLUE,TEST,RESET,str)
	}
}
//
func Warn(str string,color bool) {
	if color{
		fmt.Printf("%s%s%s %s%s%s\n",RED,WARN,RESET,RED,str,RESET)
	} else{
		fmt.Printf("%s%s%s %s\n",RED,WARN,RESET,str)
	}
}
//
func Ask(str string,color bool) {
	if color{
		fmt.Printf("%s%s%s %s%s%s\n",CYAN,ASK,RESET,CYAN,str,RESET)
	} else{
		fmt.Printf("%s%s%s %s\n",CYAN,ASK,RESET,str)
	}
}

var (
	_url      = flag.String("u","","\t\tSet target URL")
	_get      = flag.Bool("g",false,"\t\tSet get method")
	_post     = flag.Bool("p",false,"\t\tSet post method")
	_data     = flag.String("d","","\t\tSet post data")
	_headers  = flag.String("H","","\t\tSet headers ('name:value,name:value')")
	_wordlist = flag.String("w","dict.txt","\t\tSet your wordlist")
	_help     = flag.Bool("h",false,"\t\tShow this Help")
)

func Banner() {
	fmt.Printf("%s    ___                         %s\n",GREEN,RESET)                   
	fmt.Printf("%s   /   |  _________  ___       %s\n",GREEN,RESET)
	fmt.Printf("%s  / /| | / ___/ __ \\/ __\\   %s\n",GREEN,RESET)
	fmt.Printf("%s / ___ |/ /  / /_/ / / / /   %s\n",GREEN,RESET)
	fmt.Printf("%s/_/  |_/_/   \\____/_/ /_/ %s(v0.1.0 beta)%s\n",GREEN,YELLOW,RESET)
	fmt.Printf("----------------------------\n")
	fmt.Printf("  Momo (M4ll0k) Outaadi \n\n") 
}

func CheckUrl(url string) string {
	// check url 
	if url != "" {
		if strings.Contains(url,"://"){
			return url
		} else {
			if strings.Contains(url,"."){
				return "http://" + url
			} else {
				Warn("Please enter with valid URL",true)
				return ""
			}
		}
	} else {
		Warn("Please enter with your URL!",true)
		return ""
	}
	return ""
}

func JoinPost(data string, param string) string {
	// Params Join
	var params = param + "=fuzz"
	if data == "" {
		return params
	} else {
		if strings.HasSuffix(data,"&") {
			return data + param + "=fuzz"
		} else {
			if strings.HasSuffix(data,"=") {
				return data + "fuzz&" + param + "=fuzz"
			} else {
				return data + "&" + param + "=fuzz"
			}
		}
	}
	return params
}

func JoinGet(url string, param string) string {
	// URL Join 
	var params = param + "=fuzz"
	if strings.HasSuffix(url,"?") {
		if strings.Contains(url,"=") {
			if strings.HasSuffix(url,"&") {
				return url + params
			} else {
				return url + "&" + params
			}
		} else {
			return url + params
		}
		return url + params
	} else {
		if strings.Contains(url,"=") {
			if strings.HasSuffix(url,"&") {
				return url + params
			} else {
				return url + "&" + params
			}
			return url + "&" + params
		} else {
			return url + "?" + params
		}
	}
	return url
}


func Request(url string, method string, data string, payload string, headers string) {
	// Do Request
	m := strings.ToLower(method)
	if m == "post" {
		// 1 req content
		f_content,f_url := Post(url,data,headers)
		// 2 req content
		s_content,s_url := Post(url,JoinPost(data,payload),headers)
		if s_content != f_content {
			if s_url == url {
				Info("Found a potentially valid parameter: ",false)
				Plus("URL  => "+s_url,false)
				Plus("POST => "+JoinPost(data,payload),false)
			} else {
				if f_url == url {
					fmt.Printf("")
				}
			}
		}
	} else {
		// 1 req content
		f_content,f_url := Get(url,headers)
		// 2 req content
		real_url := JoinGet(url,payload)
		s_content,s_url := Get(real_url,headers)
		if s_content != f_content {
			if s_url == real_url {
				Info("Found a potentially valid parameter: ",false)
				Plus("URL => " + s_url,false)
			} else {
				if s_url == f_url {
					fmt.Printf("")
				}
			}
		}
	}
}


func Get(url string,headers string) (string,string) {
	// create new request
	req,err := http.NewRequest("GET",url,nil)
	req.Header.Set("User-Agent","curl/7.64.1")
	// add headers
	if headers != "" {
		list := strings.Split(headers,",")
		for _,value := range list {
			r := strings.Split(value,":")
			req.Header.Set(string(r[0]),string(r[1]))
		}
	}
	// client
	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
			},
	}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	} else {
		defer resp.Body.Close()
		content, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		}
		return string(content),resp.Request.URL.String()
	}
	return "",""
}

func Post(url string, data string,headers string) (string,string) {
	post_data := []byte(data)
	// create new request
	req, err := http.NewRequest("POST",url,bytes.NewBuffer(post_data))
	req.Header.Set("User-Agent","curl/7.64.1")
	// add headers
	if headers != "" {
		list := strings.Split(headers,",")
		for _,value := range list {
			r := strings.Split(value,":")
			req.Header.Set(string(r[0]),string(r[1]))
		}
	}
	// client
	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	resp,err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	content, _ := ioutil.ReadAll(resp.Body)
	return string(content),resp.Request.URL.String()
}

func main() {
	// Main 
	flag.Parse()
	uri := *_url
	help := *_help
	// * 
	if uri == "" || help == true {
		flag.Usage()
		return
	}
	Banner()
	// time 
	t := time.Now()
	time_now := t.Format("2006-01-02 15:04:05")
	Plus("URL: "+*_url,false)
	Plus("Starting: "+time_now,false)
	fmt.Printf("\n")
	// end time
	file,err := os.Open(*_wordlist)
	if err != nil {
		Warn("Error: \""+*_wordlist+"\" not found!!",true)
		return
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	uri = CheckUrl(*_url)
	if uri == "" {
		return
	}
	Test("Bruteforcing...",true)
	headers := *_headers
	if *_get {
		// read payload
		for scanner.Scan() {
			Request(uri,"GET","",scanner.Text(),headers)
		}
		// 
	} else {
		if *_post { 
			// read payload 
			for scanner.Scan() {
				Request(uri,"POST",*_data,scanner.Text(),headers)
			}
		}
	}
	Test("Done!",true)
}
