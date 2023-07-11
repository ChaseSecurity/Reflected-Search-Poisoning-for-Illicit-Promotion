from typing import Set
from bs4 import BeautifulSoup
import re
from urllib import parse
from create_proxy_auth_extension import create_proxy_auth_extension
import requests
# from selenium import webdriver
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
            '我们的系统检测到您网络中存在异常访问请求' not in browser.page_source):
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
            '我们的系统检测到您网络中存在异常访问请求' not in res.text):
            # print(res.text)
            return res.text
        else:
            # print(res.text)
            return ''
    except:
        return ""


def isFreeRide(title:str, link:str):
    if title.startswith('http://') or title.startswith('https://') or 'sogoucdn.com' in link:
        return False
    if link.startswith('http'):
        if parse.urlparse(link).hostname == title.split(':')[0]:
            return False
        elif '%' in link or not link.isascii():
            return True
        else:
            return False
    else:
        return False


def get_kwd_from_url(link):
    link_split = re.split('[?&=/]', link)
    message_origin = max(link_split, key=len, default='')
    message = parse.unquote(message_origin)
    return message



def parse_html(page_source, results: set , results_output:set, keyword, page_num):
    soup = BeautifulSoup(page_source, "html.parser")
    try:
        search_results = soup.find_all('div', class_ = 'results')[0]
    except Exception as e:
        return False
    anchors = search_results.find_all('a')
    if len(anchors) > 0:
        for anchor in anchors:
            try:
                if '/link' in anchor['href']:
                    link = get_real_address('https://www.sogou.com' + anchor['href'])
                else:
                    link = anchor['href']
                title = get_kwd_from_url(link)
                timestump = time.time()
                if link.startswith('http') and 'snapshot.sogou' not in link:
                    if (title, link) not in results:
                        results_output.add((title, link, keyword, page_num, timestump))
                        results.add((title, link))
            except:
                pass
        return True
    else:
        return False


def get_real_address(url):
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, allow_redirects=False)
        pattern1 = r'window\.location\.replace\("(.*?)"\)'
        loc1 = re.search(pattern1, res.text).group()
        pattern2 = r'\"(.*?)\"'
        loc2 = re.search(pattern2, loc1).group()
        real_url = loc2[1:-1]
        return real_url
    except:
        return url
    