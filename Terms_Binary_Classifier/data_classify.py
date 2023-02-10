from random import sample
import logging
from util import *
from classifier_util import *
import pickle
import warnings
from urllib import parse
logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore")

with open('adaboost_model.pickle', 'rb') as f:
    model = pickle.load(f)

with open('data_for_classify/data.txt', 'r', encoding='utf-8') as fp:
    all_data = fp.readlines()

data_terms = []
positive_data_predicted = []
negative_data_predicted = []
for item in all_data:
    data_terms.append(eval(item)[0])

logging.info('Finish pre-proceeding')

predict_results = Predict_With_Model(model, data_terms)

for index, result in enumerate(predict_results):
    turp = eval(all_data[index])
    term = turp[0]
    link = turp[1]
    if result == 1:
        positive_data_predicted.append(all_data[index])
    else:
        negative_data_predicted.append(all_data[index])

logging.info(f'Finish predict, with positive {len(positive_data_predicted)}, negative {len(negative_data_predicted)}')
with open('data_for_classify/data_negative.txt', 'w', encoding='utf-8') as fp:
    for item in negative_data_predicted:
        fp.write(item)

with open('data_for_classify/data_positive.txt', 'w', encoding='utf-8') as fp:
    for item in positive_data_predicted:
        fp.write(item)

logging.info('Finish saving')