import json
import csv
import argparse
import logging
import time

data_base_dir = "/data2/sangyiwu/RBSEO_Cybercrime_TimeMachine/output_website"

def is_download_related(content):
    keywords = ['下载', '安卓app', '苹果app', 'download', 'androidapp', 'iosapp', 'androiddown', 'downapp', 'appbtn', 'downbtn', 'downsoft']
    content.lower()
    content.replace('_', '').replace('-', '').replace(' ', '')
    for keyword in keywords:
        if keyword in content:
            return (True, keyword)
    return (False, '')

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    parser = argparse.ArgumentParser("App Likeliness")
    parser.add_argument("date", type=str, help="result_stats_DATE.json")
    options = parser.parse_args()

    res_stat_file = f"result_stats_{options.date}.json"
    res_stats = []
    try:
        start_time = time.time()
        with open(f"{data_base_dir}/{res_stat_file}", "r", encoding="utf-8") as fd:
            logging.info(f"Inited {options.date}")
            lines = fd.readlines()
            for line in lines:
                res_stat = json.loads(line)
                res_stats.append(res_stat)

        result = []
        total = 0
        domains = set()
        domains_app = set()
        for res_stat in res_stats:
            if res_stat['is_success'] == True:
                total += 1
                domains.add(res_stat['domain'])

                res_dir = f"{data_base_dir}/{res_stat['provider']}/{res_stat['result_basedir']}"
                har_file_path = f"{res_dir}/test.har"
                (app_likely, keyword) = (False, '')
                
                with open(har_file_path, "r", encoding="utf-8") as har_file:
                    har_data = json.load(har_file)

                    for entry in har_data['log']['entries']:
                        if 'response' in entry:
                            response = entry['response']
                            if 'content' in response:
                                content = response['content']
                                if 'text' in content:
                                    if content['mimeType'] == 'text/html':
                                        (app_likely, keyword) = is_download_related(content['text'])
                                        if app_likely == True:
                                            result.append([res_stat['domain'], res_stat['result_basedir']])
                                            domains_app.add(res_stat['domain'])
                                            break
        logging.info(f"Among {total} urls, {len(result)}({len(result)/total}) may contain APP download content.")
        logging.info(f"Among {len(domains)} domains, {len(domains_app)}({len(domains_app)/len(domains)}) may contain APP download content.")
        
        with open(f"app_{options.date}.csv", "w", encoding="utf-8", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['domain', 'result_dir'])
            csvwriter.writerows(result)
        logging.info(f"Results have been written to the file app_{options.date}.csv.")
        logging.info(f"Done {options.date} with the cost of {time.time()-start_time} seconds.")
    
    except Exception as e:
        logging.warning(e)
        exit()