import logging
from util import *
import pickle
import warnings
from sklearn.ensemble import RandomForestClassifier

# scikit-learn == 0.21.3

logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore")

with open('random_forest_model_keywords.pickle', 'rb') as f:
    model = pickle.load(f)

with open('positive_promotions.txt', 'r', encoding='utf-8') as fp:
    positive_terms = fp.read().splitlines()


keywords_all = set()
for item in positive_terms:
    term = eval(item)[0]
    pattern = r'[\{\}\[\]【】()『』（）<>《》☀️👉_⋘⋙\|✍█⚡〖〗\n「」]'
    keyword_term_tmp = re.split(pattern, term)
    for string in keyword_term_tmp:
        if string != '':
            keywords_all.add(string)

keywords_all_list = []
positive_keywords_predicted = []
negative_keywords_predicted = []
for item in keywords_all:
    keywords_all_list.append(item[:-1])

logging.info('Finish pre-proceeding')

predict_results = Predict_Keywords_With_Model(model, keywords_all_list)

for index, result in enumerate(predict_results):
    if result == 1:
        positive_keywords_predicted.append(keywords_all_list[index])
    else:
        negative_keywords_predicted.append(keywords_all_list[index])

logging.info(f'Finish predict, with positive {len(positive_keywords_predicted)}, negative {len(negative_keywords_predicted)}')

with open('keywords_extracted.txt', 'w', encoding='utf-8') as fp:
    for item in positive_keywords_predicted:
        fp.write(item)
        fp.write('\n')

logging.info('Finish saving')