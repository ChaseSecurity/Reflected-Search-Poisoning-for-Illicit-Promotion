from util import *
from random import randint
import warnings
from classifier import *
import pickle
import logging
import threading
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

warnings.filterwarnings("ignore")

with open('model/adaboost_model.pickle', 'rb') as f:
    model = pickle.load(f)

def search_a_site(site, port):
    proxyPort = port
    proxies = {
        'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort),
        'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort)
    }
    insite_SE = site
    url = "https://www.google.com/search?q=site:" +insite_SE+ "&start=0"
    result_list = []

    still_Have_Result = True
    start_num = 0
    page_source = ''
    while still_Have_Result:
        url = "https://www.google.com/search?q=site:" +insite_SE+ "&start=" + str(start_num)
        page_source = get_html_using_requests(url, proxies)
        start_try_time = time.time()
        while page_source == '':
            if time.time() - start_try_time > 120:
                proxies = {
                    'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19)),
                    'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19))
                }
                # If wait for more that 120s, then choose a new proxy port. 
                # Never suspended by a bad proxy!
            page_source = get_html_using_requests(url, proxies)
        still_Have_Result = parse_html(page_source, result_list, 'site:'+insite_SE, start_num // 10)
        start_num += 10
        page_source = ''

    data_terms = []
    all_data_for_classify = []
    positive_data_predicted = []
    negative_data_predicted = []
    for result in result_list:
        if isFreeRide(result[0], result[1]):
            all_data_for_classify.append(str(result))
        else:
            negative_data_predicted.append(str(result))
            
    for item in all_data_for_classify:
        data_terms.append(eval(item)[0])

    if len(all_data_for_classify) != 0:
        predict_results = Predict_With_Model(model, data_terms)

        for index, result in enumerate(predict_results):
            if result == 1:
                positive_data_predicted.append(all_data_for_classify[index])
            else:
                negative_data_predicted.append(all_data_for_classify[index])
    positive_result_num = len(positive_data_predicted)
    lock.acquire()
    with open('result/negative_data_predicted_fromsite.txt', 'a', encoding='utf-8') as fp:
        for item in negative_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open('result/positive_data_predicted_fromsite.txt', 'a', encoding='utf-8') as fp:
        for item in positive_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open('result/result_from_site.txt', 'a', encoding='utf-8') as fp:
        result_len = len(result_list)
        for i in range(result_len):
            fp.write(str(result_list[i]))
            fp.write('\n')
    print('Finish crawling freerided site: ' + site + ' result num = ' + str(result_len))
    lock.release()
    # If result len < 50, then try to add some keywords
    if positive_result_num < 50:
        keywords = ['微', '薇', '扣', 'qq', 'vx', 'tg', 'telegram',  '飞机', '@', '网', '复制']
        for i, keyword in enumerate(keywords):
            # thread_pool.submit(search_a_site_with_keywords, site, keyword, 10000 + (i % 5))
            search_a_site_with_keywords(site, keyword, 10000 + (i % 20))


def search_a_site_with_keywords(site, keyword, port):
    proxyPort = port
    proxies = {
        'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort),
        'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort)
    }
    insite_SE = site
    url = 'https://www.google.com/search?q='+keyword+'+site:' +insite_SE+ '&start=0'
    still_Have_Result = True
    start_num = 0
    page_source = ''
    result_list = []
    while still_Have_Result:
        url = 'https://www.google.com/search?q='+keyword+'+site:' +insite_SE+ '&start=' + str(start_num)
        page_source = get_html_using_requests(url, proxies)
        start_try_time = time.time()
        while page_source == '':
            if time.time() - start_try_time > 120:
                proxies = {
                    'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19)),
                    'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19))
                }
            page_source = get_html_using_requests(url, proxies)
                # If wait for more that 120s, then choose a new proxy port. 
                # Never suspended by a bad proxy! 
        still_Have_Result = parse_html(page_source, result_list, keyword+'+site:'+insite_SE, start_num // 10)
        start_num += 10
        page_source = ''
    data_terms = []
    all_data_for_classify = []
    positive_data_predicted = []
    negative_data_predicted = []
    for result in result_list:
        if isFreeRide(result[0], result[1]):
            all_data_for_classify.append(str(result))
        else:
            negative_data_predicted.append(str(result))
    
    for item in all_data_for_classify:
        data_terms.append(eval(item)[0])

    if len(all_data_for_classify) != 0:
        predict_results = Predict_With_Model(model, data_terms)

        for index, result in enumerate(predict_results):
            if result == 1:
                positive_data_predicted.append(all_data_for_classify[index])
            else:
                negative_data_predicted.append(all_data_for_classify[index])
    positive_result_num = len(positive_data_predicted)
    lock.acquire()
    with open('result/negative_data_predicted_fromsite.txt', 'a', encoding='utf-8') as fp:
        for item in negative_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open('result/positive_data_predicted_fromsite.txt', 'a', encoding='utf-8') as fp:
        for item in positive_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open('result/result_from_site.txt', 'a', encoding='utf-8') as fp:
        result_len = len(result_list)
        for i in range(result_len):
            fp.write(str(result_list[i]))
            fp.write('\n')
    lock.release()
    print('Finish crawling freerided site: ' + site + ' result num = ' + str(result_len) + ' with keyword ' + keyword)


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor, as_completed
    max_pool = 600
    thread_pool = ThreadPoolExecutor(max_workers=max_pool)
    with open('result/SE_Link.txt', 'r', encoding='utf-8') as fp:
        SE_link = fp.readlines()

    all_task = []
    site_index = 0
    start_with_index = 0
    for item in SE_link:
        site_index += 1
        if site_index < start_with_index:
            continue
        if len(all_task) < max_pool:
            all_task.append(thread_pool.submit(search_a_site, item[:-1], 10000 + (site_index % 20)))
            logging.info(f'Initial Submit index = {site_index}')
        else:
            for future in as_completed(all_task):
                all_task.remove(future)
                all_task.append(thread_pool.submit(search_a_site, item[:-1], 10000 + (site_index % 20)))
                logging.info(f'Finished, Submit index = {site_index}')
                break
    for future in as_completed(all_task):
        logging.info(f'Finish. ')
