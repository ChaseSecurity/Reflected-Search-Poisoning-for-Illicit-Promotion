from util import *
from random import randint
import warnings
import logging
import threading
import pickle
from classifier import *
lock = threading.Lock()

logging.basicConfig(level=logging.INFO)

use_browser = False
use_proxy = False
warnings.filterwarnings("ignore")
with open('model/adaboost_model.pickle', 'rb') as f:
    model = pickle.load(f)

def search_a_contact(contact, port):
    proxyPort = port
    if use_proxy:
        proxies = {
            'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort),
            'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort)
        }
    else:
        proxies = None
    url = "https://www.bing.com/search?q=" +contact+ "&start=0&FORM=PERE"
    results_output = set()
    results = set()

    Have_Result = True
    start_num = 1
    page_source = ''
    for i in range(15):
        url = "https://www.bing.com/search?q=" +contact+ "&first=" + str(start_num) + '&FORM=PERE'
        page_source = get_html_using_requests(url, proxies)
        while page_source == '':
            page_source = get_html_using_requests(url, proxies)
        Have_Result = parse_html(page_source, results, results_output, contact, start_num // 10)
        start_num += 10
        page_source = ''
        if not Have_Result:
            break

    data_terms = []
    all_data_for_classify = []
    positive_data_predicted = []
    negative_data_predicted = []
    for result in results_output:
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

    lock.acquire()
    with open('result/negative_data_predicted.txt', 'a', encoding='utf-8') as fp:
        for item in negative_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open('result/positive_data_predicted.txt', 'a', encoding='utf-8') as fp:
        for item in positive_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open('result/result_from_contact.txt', 'a', encoding='utf-8') as fp:
        result_len = len(results_output)
        for result in results_output:
            fp.write(str(result))
            fp.write('\n')
    lock.release()
    print(f'Finish contact info: {contact}, result num = {result_len}, positive num = {len(positive_data_predicted)}')


from concurrent.futures import ThreadPoolExecutor, as_completed
max_pool = 100
thread_pool = ThreadPoolExecutor(max_workers=max_pool)
if __name__ == '__main__':
    with open('result/contact.txt', 'r', encoding='utf-8') as fp:
        contact_list = fp.readlines()

    all_task = []
    contact_index = 0
    start_with_index = 0
    for contact in contact_list:
        contact_index += 1
        if contact_index < start_with_index:
            continue
        if len(all_task) < max_pool:
            all_task.append(thread_pool.submit(search_a_contact, contact[:-1], 10000 + (contact_index % 20)))
            logging.info(f'Initial Submit index = {contact_index}')
        else:
            for future in as_completed(all_task):
                all_task.remove(future)
                all_task.append(thread_pool.submit(search_a_contact, contact[:-1], 10000 + (contact_index % 20)))
                logging.info(f'Finished, Submit index = {contact_index}')
                break
    for future in as_completed(all_task):
        logging.info(f'Finish. ')