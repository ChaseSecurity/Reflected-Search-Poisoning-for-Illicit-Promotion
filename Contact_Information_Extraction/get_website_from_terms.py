import re
import csv
import dns.resolver
import logging
import threading
lock = threading.Lock()

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

terms_with_website = set()

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

url_pattern = r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})*\.[a-zA-Z]{2,62}'

urls = {}
dns_failed = set()

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

def get_website(term, index):
    try:
        term_replaced = term.replace('·', '.')
        # term_replaced = term_replaced.replace('-', '.')
        term_replaced = term_replaced.replace('༚', '.')
        term_replaced = term_replaced.replace('。', '.')
        term_replaced = term_replaced.replace('点', '.')
        term_replaced = term_replaced.replace('쩜', '.')
        term_replaced = term_replaced.replace('․', '.')
        term_replaced = term_replaced.replace('㏄', 'cc')
        term_replaced = term_replaced.replace('⒑', '10.')
        term_replaced = term_replaced.replace('⒒', '11.')
        term_replaced = term_replaced.replace('⒓', '12.')
        term_replaced = term_replaced.replace('⒔', '13.')
        term_replaced = term_replaced.replace('⒕', '14.')
        term_replaced = term_replaced.replace('⒖', '15.')
        term_replaced = term_replaced.replace('⒗', '16.')
        term_replaced = term_replaced.replace('⒘', '17.')
        term_replaced = term_replaced.replace('⒙', '18.')
        term_replaced = term_replaced.replace('⒚', '19.')
        term_replaced = term_replaced.replace('⒛', '20.')
        url = re.search(url_pattern, term_replaced).group().lower()
        if is_legal_url(url) and not term.startswith('http://') and not term.startswith('https://'):
            # Sometimes term is a whole url starts with http://, this is often a redirecting url embedding in origin url, 
            # instead of a SEO term. 
            # Actually this is a false positive term misclassified by our adaboost classifier. 
            # Jump over when extracting url from terms. 
            if url not in urls.keys() and url not in dns_failed:
                isDnsSuccess =  try_dns(url)
            lock.acquire()
            if url not in dns_failed:
                if url not in urls.keys():
                    if isDnsSuccess:
                        urls[url] = [term, 1]
                        terms_with_website.add(term)
                    else:
                        dns_failed.add(url)
                else:
                    urls[url][1] += 1
                    terms_with_website.add(term)
            lock.release()
        if index % 10000 == 1:
            print('finish term ' + str(index))
    except:
        if index % 10000 == 1:
            print('finish term ' + str(index))
        return

from concurrent.futures import ThreadPoolExecutor
thread_pool = ThreadPoolExecutor(max_workers=20)
    
for index, term in enumerate(terms):
    thread_pool.submit(get_website, term, index)


thread_pool.shutdown(wait= True)
with open('data/urls_from_terms.txt', 'w', encoding='utf-8') as fp:
    url_list = []
    for url in urls:
        url_list.append((url, urls[url][0], urls[url][1]))

    url_list.sort(key=lambda x: -x[2])
    for data in url_list:
        fp.write(str(data))
        fp.write('\n')


with open('data/terms_with_website.txt', 'w', encoding='utf-8') as fp:
    for item in terms_with_website:
        fp.write(item)
        fp.write('\n')

pass