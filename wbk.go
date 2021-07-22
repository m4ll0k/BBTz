package main

/*
** name: wbk (waybackurls)
** cred: https://github.com/tomnomnom/hacks/tree/master/waybackurls
** docs: https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server#url-match-scope
** m4ll0k (github.com/m4ll0k)

DOC LINK: https://bit.ly/2UCEIyH

main features compared to gau / waybackurls:

filtring (https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server#filtering):
  Date Range:
  E.g:
	  $ wbk -fromto "2010-2015" paypal.com

  Regex filtering
  E.g:
	  $ wbk -filter "statuscode:200,mimetype:application/json" paypal.com     # show only urls with statuscode 200 and mimetype application/json
	  $ wbk -filter "\!statuscode:200,\!mimetype:application/json" paypal.com # not show urls with statuscode 200 and mimetype application/json

url match scope (https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server#url-match-scope)
	E.g:
	  $ wbk -match "exact" paypal.com/signin
	  $ wbk -match "host"  paypal.com
	  $ ...

inputs
	E.g:
		$ cat mydomains.txt | wbk ... # stdin
		$ wbk ... mydomains.txt       # file
		$ wbk ... mydomain.com        # string


*/

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

const VERSION = "v0.1 (beta)"
const fetchCDX = "http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=json&fl=original&collapse=urlkey"

var (
	_fromto  = flag.String("fromto", "", "\nresults filtered by timestamp using from= and to= params\nE.g:\n-fromto \"2012-2015\"\n")
	_filter  = flag.String("filter", "", "\nfilter:\n\tmimetype:\tE.g: mimetype:application/json\n\tstatuscode:\tE.g: statuscode:200\nE.g:\n-filter \"mimetype:application/json\"\n")
	_match   = flag.String("match", "", "\n\texact\n\tprefix\n\thost\n\tdomain\n")
	_version = flag.Bool("version", false, "show version and exit\n\nDoc link: https://bit.ly/2UCEIyH\n")
)

func main() {
	// main
	var domains []string

	var targets []string

	matchTypies := map[string]bool{
		"exact":  true,
		"prefix": true,
		"host":   true,
		"domain": true,
	}

	filterTypies := map[string]bool{
		"statuscode":  true,
		"mimetype":    true,
		"!statuscode": true,
		"!mimetype":   true,
		"digest":      true,
		"!digest":     true,
	}

	fetchCDXS := ""
	flag.Parse()

	filter := *_filter
	fromto := *_fromto
	match := *_match

	if *_version {
		fmt.Fprint(os.Stdout, "WBK version: ", VERSION, "\n")
		os.Exit(0)
	}

	if flag.NArg() > 0 {

		domains = []string{flag.Arg(0)}
		_, b := os.Stat(domains[0])

		if b != nil {
			targets = domains
		} else /* read file */ {
			file, err := os.Open(domains[0])
			if err != nil {
				fmt.Fprint(os.Stderr, "Error: ", err, "\n")
			}
			read_file := bufio.NewScanner(file)
			for read_file.Scan() {
				targets = append(targets, read_file.Text())
			}

		}
	} else /* read from stdin */ {
		stdin_input := bufio.NewScanner(os.Stdin)
		for stdin_input.Scan() {
			targets = append(targets, stdin_input.Text())
		}
		if err := stdin_input.Err(); err != nil {
			fmt.Fprint(os.Stderr, "", err, "\n")
		}
	}

	fetchCDXS = fetchCDX

	if strings.Contains(fromto, "-") {
		fetchCDXS = fetchCDXS + "&from=" + strings.Split(fromto, "-")[0] + "&to=" + strings.Split(fromto, "-")[1]
	}
	if filter != "" {
		filters := strings.Split(filter, ",")
		params := ""
		for _, v := range filters {
			if filterTypies[strings.Split(v, ":")[0]] {
				params = params + "&filter=" + v
			}
		}
		fetchCDXS = fetchCDXS + params
	}

	if matchTypies[match] {
		fetchCDXS = fetchCDXS + "&matchType=" + match
	}

	for _, domain := range targets {
		urls, err := getContent(fetchCDXS, domain)
		if err != nil {
			fmt.Fprintf(os.Stderr, "failed to fetch URLs\n")
			continue
		}

		for _, url := range urls {
			fmt.Println(url)
		}
	}

}

func getContent(fetchCDXS string, domain string) ([]string, error) {
	// get content
	fetch := fmt.Sprintf(fetchCDXS, domain)
	out := make([]string, 0)

	res, err := http.Get(fetch)

	if err != nil {
		return out, err
	}

	raw, err := ioutil.ReadAll(res.Body)
	res.Body.Close()

	if err != nil {
		return out, err
	}

	var wrapper [][]string
	err = json.Unmarshal(raw, &wrapper)
	skip := true

	for _, urls := range wrapper {
		if skip {
			skip = false
			continue
		}
		out = append(out, urls...)
	}

	return out, nil
}
