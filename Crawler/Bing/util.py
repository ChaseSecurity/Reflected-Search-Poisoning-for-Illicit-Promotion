from bs4 import BeautifulSoup
import re
from urllib import parse
from create_proxy_auth_extension import create_proxy_auth_extension
import requests
from selenium import webdriver
import time

def get_html(url, browser):
    # time.sleep(5 * random.random())
    try:
        res= browser.get(url)
        browser.encoding = 'utf-8'
        if('This page isn’t working' not in browser.page_source and\
            '该网页无法正常运作' not in browser.page_source and\
            'Check your Internet connection' not in browser.page_source and\
            '请检查您的互联网连接是否正常' not in browser.page_source and \
            'Search' in browser.page_source):
            # print('\n')
            # print(browser.page_source)
            # print('\n')
            return browser.page_source
        else:
            # time.sleep(20)
            # print(browser.page_source)
            return ''
    except:
        return ""


def get_html_using_requests(url, proxies):
    try:
        headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        res = requests.get(url=url, proxies=proxies, headers=headers, verify=False)
        if('This page isn’t working' not in res.text and\
            '该网页无法正常运作' not in res.text and\
            'Check your Internet connection' not in res.text and\
            '请检查您的互联网连接是否正常' not in res.text and \
            'Search' in res.text):
            # print(res.text)
            return res.text
        else:
            # print(res.text)
            return ''
    except:
        return ""


def isFreeRide(title, link):
    if ('%' in link) and (link.startswith('http')):
        if parse.urlparse(link).hostname == title:
            return False
        else:
            return True
    else:
        return False


def get_kwd_from_url(link):
    link_split = re.split('[?&=/]', link)
    message_origin = max(link_split, key=len, default='')
    message = parse.unquote(message_origin)
    return message



def parse_html(page_source, results: set , results_output:set, keyword, page_num):
    if 'There are no results for' in page_source:
        return False
    else:
        soup = BeautifulSoup(page_source, "html.parser")
        search_results = soup.find_all('ol', id = 'b_results')[0]
        anchors = search_results.find_all('a')
        for anchor in anchors:
            try:
                link = anchor['href']
                title = get_kwd_from_url(link)
                timestump = time.time()
                if link.startswith('http'):
                    if (title, link) not in results:
                        results_output.add((title, link, keyword, page_num, timestump))
                        results.add((title, link))
            except:
                pass
        return True
