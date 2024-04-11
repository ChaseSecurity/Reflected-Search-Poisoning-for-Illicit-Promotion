import pickle
import re
import warnings
import logging
import argparse
from classifier import *

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, required=True, help='The keywords extracted output file')
parser.add_argument('--result_dir', type=str, required=True, help='The obtained crawling results directory')
parser.add_argument('--model_dir', type=str, default='./model', help='The IPT_keyword_extractor directory')
args = parser.parse_args()

output_file = args.output
result_dir = args.result_dir
model_dir = args.model_dir

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

#split keywords from terms
keywords_set = set()
for item in positive_terms_predicted:
    pattern = r'[\{\}\[\]【】()『』（）<>《》☀️👉_⋘⋙\|✍█⚡〖〗\n「」]'
    keyword_term_tmp = re.split(pattern, item)
    for string in keyword_term_tmp:
        if string != '':
            keywords_set.add(string)
keywords_list = [item for item in keywords_set]
logging.info(f'Finish spliting, get total keywords {len(keywords_list)}')

#--------------------------------------------------------------------------------
#involve the queried keywords classifier
positive_keywords_predicted = []
with open('model/random_forest_model_keywords.pickle', 'rb') as f:
    model = pickle.load(f)

predict_results = Predict_Keywords_With_Model(model, keywords_list)
for index, result in enumerate(predict_results):
    if result == 1:
        positive_keywords_predicted.append(keywords_list[index])

logging.info(f'Finish keywords classifying, {len(positive_keywords_predicted)} positive in {len(keywords_list)} results')

#---------------------------------------------------------------------------------
# Write to files
keywords_set = set()
for contact in positive_keywords_predicted:
    keywords_set.add(contact)

with open(output_file, 'w', encoding='utf-8') as fp:
    for i, item in enumerate(keywords_set):
        fp.write(item)
        fp.write('\n')

logging.info('Finish all. ')
pass