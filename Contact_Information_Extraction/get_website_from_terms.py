import re
import csv
import dns.resolver
import logging

logging.basicConfig(level=logging.INFO)

data = []

with open('data/Google/positive_data_predicted_fromcontact.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Google/positive_data_predicted_fromsite.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Bing/positive_data_predicted.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Baidu/positive_data_predicted.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Sogou/positive_data_predicted.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

terms = set()
for item in data:
    term, link, kwd, timestamp, pagenum = eval(item)
    terms.add(term)

print(f'Finish Getting terms, get {len(terms)} terms')

top_domain = set()
with open('top_domain.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp)
    for item in reader:
        try:
            top_domain.add(item[0])
        except:
            pass

url_pattern = r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?'

urls_origin = set()

def is_legal_url(url:str):
    dns = url.split('.')
    if '.' + dns[-1] not in top_domain:
        return False
    return True

def try_dns(url:str):
    try:
        dns.resolver.resolve(url, 'A')
        return True
    except:
        return False

for term in terms:
    try:
        url = re.search(url_pattern, term).group().lower() 
        if is_legal_url(url):
            if url not in urls_origin:
                urls_origin.add(url)
    except:
        pass

logging.info(f'Get origin urls: {len(urls_origin)}')

urls = set()

def add_to_urls(url, index):
    if try_dns(url):
        urls.add(url)
        logging.info(f'Accept: {url}, for {index+1} in {len(urls_origin)}')
    else:
        logging.info(f'Refuse: {url}, for {index+1} in {len(urls_origin)}')


from concurrent.futures import ThreadPoolExecutor
thread_pool = ThreadPoolExecutor(max_workers=100)
for index, url in enumerate(urls_origin):
    thread_pool.submit(add_to_urls, url, index)

thread_pool.shutdown(wait= True)
with open('data/urls_from_terms.txt', 'w', encoding='utf-8') as fp:
    for url in urls:
        fp.write(url)
        fp.write('\n')


pass