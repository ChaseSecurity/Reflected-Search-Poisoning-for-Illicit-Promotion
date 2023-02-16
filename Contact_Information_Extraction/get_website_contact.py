import re
import csv
import dns.resolver
import logging
import threading
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import numpy as np
import pandas as pd
import csv
import torch
lock = threading.Lock()

USE_DNS = False
classify_model_path = '/data/jlxue/RBSEO_contact_classifier_train_model'

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
terms_extracted = set()
terms = set()
for item in data:
    term, link, kwd, timestamp, pagenum = eval(item)
    terms.add(term)

print(f'Finish Getting terms, get {len(terms)} terms')
data = []
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
        term_replaced = term_replaced.replace('ͺ', '.')
        term_replaced = term_replaced.replace('¸', '.')
        term_replaced = term_replaced.replace('点', '.')
        term_replaced = term_replaced.replace('쩜', '.')
        term_replaced = term_replaced.replace('․', '.')
        term_replaced = term_replaced.replace('、', '.')
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
                if USE_DNS:
                    isDnsSuccess =  try_dns(url)
                else:
                    isDnsSuccess =  True
            lock.acquire()
            if url not in dns_failed:
                if url not in urls.keys():
                    if isDnsSuccess:
                        urls[url] = [term, 1]
                        terms_with_website.add(term)
                        terms_extracted.add((term, url))
                    else:
                        dns_failed.add(url)
                else:
                    urls[url][1] += 1
                    terms_with_website.add(term)
                    terms_extracted.add((term, url))
            lock.release()
        if index % 10000 == 1 and USE_DNS:
            print('finish term ' + str(index))
    except:
        if index % 10000 == 1 and USE_DNS:
            print('finish term ' + str(index))
        return

from concurrent.futures import ThreadPoolExecutor
thread_pool = ThreadPoolExecutor(max_workers=20)


labels_list = ['website', 'wechat', 'qq', 'telegram', 'others','telephone']
labels_dict = {'website':0, 'wechat':1, 'qq':2, 'telegram':3, 'others':4, 'telephone':5}

def get_website_contact(terms_all_list):
    cuda_available = torch.cuda.is_available()

    args = ClassificationArgs(eval_batch_size = 32, use_multiprocessing_for_evaluation=False)
    model = ClassificationModel('roberta', classify_model_path, num_labels=len(labels_list), use_cuda=cuda_available, args = args)

    website_terms = []
    predictions, raw_outputs = model.predict(terms_all_list)

    for index, term in enumerate(terms_all_list):
        if labels_list[predictions[index]] == 'website':
            website_terms.append(term)

    print(f'Finish contact classification, get website term {len(website_terms)}')

    for index, term in enumerate(website_terms):
        thread_pool.submit(get_website, term, index)

num = 0
index_term = 0
terms_all_list = []
for item in terms:
    num += 1
    index_term += 1
    terms_all_list.append(item)
    if num >= 50000:
        print(f'Get {len(terms_all_list)} positive terms')
        get_website_contact(terms_all_list)
        logging.info(f'Finished terms {index_term} of {len(terms)} for extracting website contact, get {len(urls)} website contacts')
        num = 0
        terms_all_list = []

print(f'Get {len(terms_all_list)} positive terms')
get_website_contact(terms_all_list)

thread_pool.shutdown(wait= True)


if USE_DNS:
    with open('data/urls_from_terms.txt', 'w', encoding='utf-8') as fp:
        url_list = []
        for url in urls:
            url_list.append((url, urls[url][0], urls[url][1]))

        url_list.sort(key=lambda x: -x[2])
        for data in url_list:
            fp.write(str(data))
            fp.write('\n')
else:
    with open('data/urls_from_terms_without_dns.txt', 'w', encoding='utf-8') as fp:
        url_list = []
        for url in urls:
            url_list.append((url, urls[url][0], urls[url][1]))

        url_list.sort(key=lambda x: -x[2])
        for data in url_list:
            fp.write(str(data))
            fp.write('\n')


if USE_DNS:
    with open('data/terms_with_website.txt', 'w', encoding='utf-8') as fp:
        for item in terms_with_website:
            fp.write(item)
            fp.write('\n')
else:
    with open('data/terms_with_website_without_dns.txt', 'w', encoding='utf-8') as fp:
        for item in terms_with_website:
            fp.write(item)
            fp.write('\n')
with open('data/terms_extracted_website.txt', 'w', encoding='utf-8') as fp:
    for item in terms_extracted:
        fp.write(str(item))
        fp.write('\n')
pass