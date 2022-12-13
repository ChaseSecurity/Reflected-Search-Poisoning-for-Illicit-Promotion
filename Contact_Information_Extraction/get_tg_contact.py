from simpletransformers.classification import ClassificationModel, ClassificationArgs
import numpy as np
import pandas as pd
from scipy.special import softmax
import csv
from simpletransformers.ner import NERModel, NERArgs
import jieba
import logging
from sklearn.metrics import f1_score,  accuracy_score
from sklearn.model_selection import train_test_split
import torch

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

NER_model_path = '/data/jlxue/RBSEO_NER_train_model'
classify_model_path = '/data/jlxue/RBSEO_contact_classifier_train_model'


def get_telegram_contact(terms_all_list, tg_contact):
    cuda_available = torch.cuda.is_available()

    args = ClassificationArgs(eval_batch_size = 32, use_multiprocessing_for_evaluation=False)
    model = ClassificationModel('roberta', classify_model_path, num_labels=len(labels_list), use_cuda=cuda_available, args = args)

    telegram_terms = []
    predictions, raw_outputs = model.predict(terms_all_list)

    for index, term in enumerate(terms_all_list):
        if labels_list[predictions[index]] == 'telegram':
            telegram_terms.append(term)

    print(f'Finish contact classification, get telegram term {len(telegram_terms)}')
    #-------------------------------------------------------------------------------------------------
    sentences = []
    sentences_raw = telegram_terms
    for term in telegram_terms:
        seg = jieba.cut(term)
        sentence = ''
        for s in seg:
            sentence += s + ' '
        sentences.append(sentence)


    # Create a NERModel
    labels = ['B-contact', 'I-contact', 'O']

    cuda_available = torch.cuda.is_available()
    args = NERArgs(use_multiprocessing_for_evaluation=False)
    model = NERModel(
        "roberta",
        NER_model_path,
        labels=labels,
        use_cuda=cuda_available,
        args=args
    )

    # # Predictions on arbitary text strings
    predictions, raw_outputs = model.predict(sentences)
    
    for n, (preds, outs) in enumerate(zip(predictions, raw_outputs)):
        result = ['', '', '', '', '']
        result[0] = sentences_raw[n]
        flag = 0
        result_index = 1
        try:
            for pred, out in zip(preds, outs):
                key = list(pred.keys())[0]
                if flag == 0:
                    if pred[key] == 'B-contact':
                        flag = 1
                        result[result_index] += key
                elif flag == 1:
                    if pred[key] == 'I-contact':
                        flag = 2
                        result[result_index] += key
                    elif pred[key] == 'O':
                        result_index += 1
                        flag = 0
                    elif pred[key] == 'B-contact':
                        result_index += 1
                        flag = 1
                        result[result_index] += key
                elif flag == 2:
                    if pred[key] == 'I-contact':
                        flag = 2
                        result[result_index] += key
                    elif pred[key] == 'O':
                        result_index += 1
                        flag = 0
                    elif pred[key] == 'B-contact':
                        result_index += 1
                        flag = 1
                        result[result_index] += key
        except:
            print("\n___________________________")
            print("Sentence: ", sentences_raw[n])
            for pred, out in zip(preds, outs):
                key = list(pred.keys())[0]
                new_out = out[key]
                preds = list(softmax(np.mean(new_out, axis=0)))
                print(key, pred[key], preds[np.argmax(preds)], preds)
        if result[1] != '' and len(result[1]) > 3 and result[1] != '@':
            if result[1] not in tg_contact.keys():
                tg_contact[result[1]] = [sentences_raw[n], 1]
            else:
                tg_contact[result[1]][1] += 1


data = []

with open('data/Google/positive_data_predicted_fromcontact.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Google/positive_data_predicted_fromsite.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Bing/positive_data_predicted.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Baidu/positive_data_predicted.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

with open('data/Sogou/positive_data_predicted.txt', 'r', encoding = 'utf-8') as fp:
    data += fp.readlines()

terms_all = set()
for item in data:
    term, link, kwd, timestamp, pagenum = eval(item)
    terms_all.add(term)

print(f'Finish Getting terms, get {len(terms_all)} terms')

#-------------------------------------------------------------------------------------------------
labels_list = ['website', 'wechat', 'qq', 'telegram', 'others']
labels_dict = {'website':0, 'wechat':1, 'qq':2, 'telegram':3, 'others':4}
terms_all_list = []
tg_contact = {}
num = 0
index_term = 0

for item in terms_all:
    num += 1
    index_term += 1
    terms_all_list.append(item)
    if num >= 50000:
        print(f'Get {len(terms_all_list)} positive terms')
        get_telegram_contact(terms_all_list, tg_contact)
        logging.info(f'Finished terms {index_term} of {len(terms_all)} for extracting telegram contact, get {len(tg_contact)} telegram contacts')
        num = 0
        terms_all_list = []


print(f'Get {len(terms_all_list)} positive terms')

get_telegram_contact(terms_all_list, tg_contact)

print(f'Finish extract telegram contact, get {len(tg_contact)}')
with open('data/telegram_contact.txt', 'w', encoding='utf-8') as fp:
    tg_list = []
    for tg in tg_contact:
        tg_list.append((tg, tg_contact[tg][0], tg_contact[tg][1]))

    tg_list.sort(key=lambda x: -x[2])
    for item in tg_list:
        fp.write(str(item))
        fp.write('\n')
