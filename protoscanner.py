# simple prototype pollution scanner 
# by m4ll0k - github.com/m4ll0k

# usage:
# cat list_of_urls.txt | python3 protoscanner.py


import sys
import threading
import argparse 

try:
    from colorama import init, Fore
except Exception as e:
    sys.exit(print('Please install colorama!'))

init(autoreset=True)

try:
    import validators
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except Exception as e:
    sys.exit(print(Fore.RED + f'Please install python lib: {e}'))

from queue import Queue
from urllib.parse import urlparse, urlunparse
from concurrent.futures import ThreadPoolExecutor, as_completed

evil_p = ['__proto__[test]=test&constructor[prototype][test]=test&__proto__.test=test#__proto__[test]=test']
total_urls = 0
total_urls_processed = 0
total_urls_lock = threading.Lock() 
url_queue = Queue()

# Function to initialize a browser instance
def initialize_browser(args):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--path {args.chromedriver}")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--enable-features=NetworkServiceInProcess")
    options.add_argument("--disable-restore-session-state")
    # ... (add other performance-related options)

    return webdriver.Chrome(options=options)

# Function to process a URL using a given browser instance
def process_url(browser):
    global total_urls_processed

    while True:
        try:
            u = url_queue.get_nowait()
        except queue.Empty:
            break

        try:
            browser.get(u)
            result = browser.execute_script("return Object.prototype.test;")

            with total_urls_lock:
                total_urls_processed += 1
                progress_percentage = (total_urls_processed / total_urls) * 100
                sys.stdout.write(f'\rProcessing {progress_percentage:.2f}% of urls..\r\t')
                sys.stdout.flush()

            if result == 'test':
                print(Fore.GREEN + f"\n[VULN]"+Fore.WHITE +"[URL]"+Fore.YELLOW +f" {u}")
        except Exception as e:
            print(Fore.RED + f"\n[ERROR] "+Fore.WHITE+f"{u}")

# Function to build URLs
def urlbuild(urls):
    final_urls = []
    for url in urls:
        if validators.url(url):
            for e in evil_p:
                try:
                    parsed_url = urlparse(url)
                    if not e.startswith('#'):
                        mod_url = parsed_url._replace(query=e)
                    else:
                        e = e[1:]
                        mod_url = parsed_url._replace(fragment=e)
                    final_url = urlunparse(mod_url)
                    if final_url not in final_urls:
                        final_urls.append(final_url)
                except Exception as e:
                    print(Fore.RED + f'Error parsing {url}: {e}')
    return final_urls

# Main function
def main(args):
    global total_urls

    urls = [line.strip() for line in args.input_file.readlines()]
    if urls == []:
        sys.exit(print(f'input file is empty!'))

    e_urls = urlbuild(urls)

    total_urls = len(e_urls)

    for u in e_urls:
        url_queue.put(u)

    batch_size = 20
    max_workers = 10

    browser_pool = [initialize_browser(args) for _ in range(max_workers)]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_url, browser) for browser in browser_pool]

        for future in as_completed(futures):
            pass

    for browser in browser_pool:
        browser.quit()

    print(Fore.GREEN + "[INFO] Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple prototype pollution scanner")
    parser.add_argument("--chromedriver", default="/opt/homebrew/bin/chromedriver", help="Path to chromedriver, default=/opt/homebrew/bin/chromedriver")
    parser.add_argument("input_file", nargs='?' ,type=argparse.FileType('r'), default=sys.stdin, help="Input file containing URLs")
    #parser.add_argument("--payload", help="Your prototype payload to test")
    #parser.add_argument("--workers", help="Thread workers")
    # Add other argparse options as needed

    args = parser.parse_args()
    main(args)
