from util import *
from classifier import *
from random import randint
import warnings
import logging
import threading
import pickle
lock = threading.Lock()
with open('model/adaboost_model.pickle', 'rb') as f:
    model = pickle.load(f)
logging.basicConfig(level=logging.INFO)

use_proxy = True
warnings.filterwarnings("ignore")

def search_a_contact(contact, port):
    proxyPort = port
    if use_proxy:
        proxies = {
            'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort),
            'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort)
        }
    else:
        proxies = None
    url = "https://www.sogou.com/web?query=" + contact + "&page=0"
    results_output = set()
    results = set()

    Have_Result = True
    start_num = 1
    page_source = ''
    for i in range(15):
        url = "https://www.sogou.com/web?query=" + contact + "&page=" + str(start_num)
        page_source = get_html_using_requests(url, proxies)
        start_try_time = time.time()
        while page_source == '':
            if time.time() - start_try_time > 120:
                proxies = {
                    'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19)),
                    'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19))
                }
            page_source = get_html_using_requests(url, proxies)
        Have_Result = parse_html(page_source, results, results_output, contact, start_num)
        start_num += 1
        page_source = ''
        if not Have_Result:
            break

    data_terms = []
    all_data = [str(result) for result in results_output]
    positive_data_predicted = []
    negative_data_predicted = []
    for item in all_data:
        data_terms.append(eval(item)[0])

    if len(all_data) != 0:
        predict_results = Predict_With_Model(model, data_terms)

        for index, result in enumerate(predict_results):
            turp = eval(all_data[index])
            term = turp[0]
            link = turp[1]
            if result == 1 and isFreeRide(term, link):
                positive_data_predicted.append(all_data[index])
            else:
                negative_data_predicted.append(all_data[index])

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
max_pool = 600
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