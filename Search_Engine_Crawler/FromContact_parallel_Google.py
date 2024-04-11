from util import *
from classifier import *
from random import randint
import warnings
import logging
import threading
import pickle
import argparse
import os
lock = threading.Lock()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--seed_path', type=str, required=True, help='The crawling seed filepath')
parser.add_argument('--result_dir', type=str, required=True, help='The crawling results directory')
parser.add_argument('--model_dir', type=str, default='./model', help='The binary_IPT_classifier directory')
args = parser.parse_args()

seed_file = args.seed_path
result_dir = args.result_dir + '/Google'
model_dir = args.model_dir
if not os.path.exists(result_dir):
    os.makedir(result_dir, exist_ok=True)

# TODO:  Fill your proxy information
proxy_user = ''
proxy_password = ''
proxy_url = ''
# proxy_port = range(10000, 10015)

with open(f'{model_dir}/random_forest_model_binaryIPT.pickle', 'rb') as f:
    model = pickle.load(f)

def search_a_contact(contact, port):
    filter = True
    proxyPort = port
    proxies = {
        'http' : f'http://{proxy_user}:{proxy_password}@{proxy_url}:' + str(proxyPort),
        'https' : f'https://{proxy_user}:{proxy_password}@{proxy_url}:' + str(proxyPort)
    }
    url = "https://www.google.com/search?q=" +contact+ "&start=0"
    if filter == False:
        url = "https://www.google.com/search?q=" +contact+ "&start=0&filter=0"
    result_list = []

    still_Have_Result = True
    start_num = 0
    page_source = ''
    while still_Have_Result:
        url = "https://www.google.com/search?q=" +contact+ "&start=" + str(start_num)
        if filter == False:
            url = "https://www.google.com/search?q=" +contact+ "&start=" + str(start_num)+'&filter=0'
        
        page_source = get_html_using_requests(url, proxies)
        start_try_time = time.time()
        while page_source == '':
            if time.time() - start_try_time > 100:
                proxies = {
                    'http' : f'http://{proxy_user}:{proxy_password}@{proxy_url}:' + str(10000+randint(0,15)),
                    'https' : f'https://{proxy_user}:{proxy_password}@{proxy_url}:' + str(10000+randint(0,15))
                }
            page_source = get_html_using_requests(url, proxies)
        still_Have_Result = parse_html(page_source, result_list, contact, start_num // 10)
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
        result_len = len(result_list)
        for i in range(result_len):
            fp.write(str(result_list[i]))
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
            all_task.append(thread_pool.submit(search_a_contact, contact[:-1], 10000+(contact_index%15)))
            logging.info(f'Initial Submit index = {contact_index}')
        else:
            for future in as_completed(all_task):
                all_task.remove(future)
                all_task.append(thread_pool.submit(search_a_contact, contact[:-1], 10000+(contact_index%15)))
                logging.info(f'Finished, Submit index = {contact_index}')
                break
    for future in as_completed(all_task):
        logging.info(f'Finish. ')