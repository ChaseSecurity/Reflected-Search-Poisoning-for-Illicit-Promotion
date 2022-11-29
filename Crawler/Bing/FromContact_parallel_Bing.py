from util import *
from random import randint
import warnings
import logging
import threading
lock = threading.Lock()

logging.basicConfig(level=logging.INFO)

use_browser = False
use_proxy = False
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

    lock.acquire()
    with open('result/result_from_contact.txt', 'a', encoding='utf-8') as fp:
        result_len = len(results_output)
        for result in results_output:
            fp.write(str(result))
            fp.write('\n')
    lock.release()
    print('Finish contact info: ' + contact + ' result num = ' + str(result_len))


from concurrent.futures import ThreadPoolExecutor, as_completed
max_pool = 150
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