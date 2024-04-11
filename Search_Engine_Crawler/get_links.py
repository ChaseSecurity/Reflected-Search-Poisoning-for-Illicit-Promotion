from urllib.parse import urlparse
import warnings
import logging
import argparse
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, required=True, help='The links extracted output file')
parser.add_argument('--result_dir', type=str, required=True, help='The obtained crawling results directory')
args = parser.parse_args()

output_file = args.output
result_dir = args.result_dir


# Read positive results from file
SEs = ['Google', 'Bing', 'Baidu', 'Sogou']
positive_terms_predicted = []
for SE in SEs:
    result_dir = args.result_dir + '/' + SE
    with open(f'{result_dir}/positive_data_predicted_from_contact.txt', 'r', encoding='utf-8') as fp:
        positive_lists = fp.readlines()
    if SE == 'Google':
        with open(f'{result_dir}/positive_data_predicted_from_site.txt', 'r', encoding='utf-8') as fp:
            positive_lists += fp.readlines()
    for item in positive_lists:
        positive_terms_predicted.append(eval(item)[0])
logging.info(f'Finish Read Data, {len(positive_terms_predicted)} positive.')

# Get the SE links
def get_SE_from_link(link):
    parse_result = urlparse(link)
    result = parse_result.scheme + '://' + parse_result.hostname
    if '%' not in parse_result.path:
        for item in parse_result.path.split('/'):
            if item != '':
                result = result + '/' + item
    else:
        for item in parse_result.path.split('/'):
            if '%' not in item:
                if item != '':
                    result = result + '/' + item
            else:
                break
    return result

links_set = set()
for result in positive_terms_predicted:
    link = get_SE_from_link(eval(result)[1])
    links_set.add(link)

# Write to file
with open(output_file, 'w', encoding='utf-8') as fp:
    for i, item in enumerate(links_set):
        fp.write(item)
        fp.write('\n')    

logging.info('Finish all. ')
pass