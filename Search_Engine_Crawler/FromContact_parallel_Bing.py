from util import *
from classifier import *
from random import randint
import warnings
import logging
import threading
import pickle
lock = threading.Lock()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore")

use_proxy = False

# TODO: Fill filepath
seed_file = ''
result_dir = ''
model_dir = ''

# TODO:  Fill your proxy information
proxy_user = ''
proxy_password = ''
proxy_url = ''
# proxy_port = range(10000, 10015)

with open(f'{model_dir}/random_forest_model_binaryIPT.pickle', 'rb') as f:
    model = pickle.load(f)

def search_a_contact(contact, port):
    proxyPort = port
    if use_proxy:
        proxies = {
        'http' : f'http://{proxy_user}:{proxy_password}@{proxy_url}:' + str(proxyPort),
        'https' : f'https://{proxy_user}:{proxy_password}@{proxy_url}:' + str(proxyPort)
        }
    else:
        proxies = None
    url = "https://www.bing.com/search?q=" +contact+ "&first=0&FORM=PERE"
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
    with open(f'{result_dir}/negative_data_predicted_from_contact.txt', 'a', encoding='utf-8') as fp:
        for item in negative_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open(f'{result_dir}/positive_data_predicted_from_contact.txt', 'a', encoding='utf-8') as fp:
        for item in positive_data_predicted:
            fp.write(item)
            fp.write('\n')

    with open(f'{result_dir}/result_from_contact.txt', 'a', encoding='utf-8') as fp:
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
    with open(seed_file, 'r', encoding='utf-8') as fp:
        contact_list = fp.readlines()

    all_task = []
    contact_index = 0
    start_with_index = 0
    for contact in contact_list:
        contact_index += 1
        if contact_index < start_with_index:
            continue
        if len(all_task) < max_pool:
            all_task.append(thread_pool.submit(search_a_contact, contact[:-1], 10000 + (contact_index % 15)))
            logging.info(f'Initial Submit index = {contact_index}')
        else:
            for future in as_completed(all_task):
                all_task.remove(future)
                all_task.append(thread_pool.submit(search_a_contact, contact[:-1], 10000 + (contact_index % 15)))
                logging.info(f'Finished, Submit index = {contact_index}')
                break
    for future in as_completed(all_task):
        logging.info(f'Finish. ')