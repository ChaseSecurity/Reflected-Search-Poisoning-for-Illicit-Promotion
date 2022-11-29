from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time
import re
from urllib import parse
from create_proxy_auth_extension import create_proxy_auth_extension
import requests

#获取网页源代码
def get_html(url, browser):
    # time.sleep(5 * random.random())
    try:
        res= browser.get(url)
        browser.encoding = 'utf-8'
        if('此网页用于确认这些请求是由您而不是自动程序发出的。' not in browser.page_source and\
         'google' in browser.page_source and\
         'This page appears when Google automatically detects requests'\
            not in browser.page_source and\
                'This page isn’t working' not in browser.page_source and\
                    '该网页无法正常运作' not in browser.page_source and\
                        'Check your Internet connection' not in browser.page_source and\
                            '请检查您的互联网连接是否正常' not in browser.page_source):
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
        if('此网页用于确认这些请求是由您而不是自动程序发出的。' not in res.text and\
         'google' in res.text and\
         'This page appears when Google automatically detects requests'\
            not in res.text and\
                'This page isn’t working' not in res.text and\
                    '该网页无法正常运作' not in res.text and\
                        'Check your Internet connection' not in res.text and\
                            '请检查您的互联网连接是否正常' not in res.text):
            # print('\n')
            # print(browser.page_source)
            # print('\n')
            # print(res.text)
            return res.text
        else:
            # time.sleep(20)
            # print(browser.page_source)
            # print(res.text)
            return ''
    except:
        return ""


def isFreeRide(title, link):
    if ('%' in link) and (link.startswith('http')) and ('google.com' not in link) and ('webcache' not in link):
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



def parse_html(page_source, result, keyword, page_num):
    soup = BeautifulSoup(page_source, "html.parser")
    search_result_div = soup.find_all('div', id = 'search')
    if len(search_result_div) == 0:
        return False
    search_result_num = len(search_result_div[0].find_all('a'))
    if search_result_num > 0:
        for search_result in search_result_div:
                anchors = search_result.find_all('a')
                for anchor in anchors:
                    try:
                        link = anchor['href']
                        title = get_kwd_from_url(link)
                        timestump = time.time()
                        if (link.startswith('http')) and ('google.com' not in link) and ('webcache' not in link):
                            result.append((title, link, keyword, page_num, timestump))
                    except:
                        continue
        return True #Get search result
    else:
        return False    #No search result