from util import *
from random import randint
import warnings
import logging
import threading
lock = threading.Lock()
logging.basicConfig(level=logging.INFO)

warnings.filterwarnings("ignore")

def search_a_contact(contact, port):
    filter = True
    proxyPort = port
    proxies = {
        'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort),
        'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(proxyPort)
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
            if time.time() - start_try_time > 120:
                proxies = {
                    'http' : 'http://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19)),
                    'https' : 'https://muxing:b1bf0c-23daaf-5f92e8-a9f151-0cf49e@private.residential.proxyrack.net:' + str(10000+randint(0, 19))
                }
            page_source = get_html_using_requests(url, proxies)
        still_Have_Result = parse_html(page_source, result_list, contact, start_num // 10)
        start_num += 10
        page_source = ''

    lock.acquire()
    with open('result/result_from_contact.txt', 'a', encoding='utf-8') as fp:
        result_len = len(result_list)
        for i in range(result_len):
            fp.write(str(result_list[i]))
            fp.write('\n')
    lock.release()
    print('Finish contact info: ' + contact + ' result num = ' + str(result_len))


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