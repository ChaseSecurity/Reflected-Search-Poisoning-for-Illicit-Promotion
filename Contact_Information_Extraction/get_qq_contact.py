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
import re

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

NER_model_path = '/data/jlxue/RBSEO_NER_train_model'
classify_model_path = '/data/jlxue/RBSEO_contact_classifier_train_model'
qq_succeed_path = '/data/jlxue/qq_succeed_classifier_model'


def get_qq_contact(terms_all_list, qq_contact):
    unicode_similar_nums = [
        '0OoΟοσОоՕօסه٥ھہە۵߀०০੦૦ଠ୦௦ం౦ಂ೦ംഠ൦ං๐໐ဝ၀ჿዐᴏᴑℴⲞⲟⵔ〇ꓳꬽﮦﮧﮨﮩﮪﮫﮬﮭﻩﻪﻫﻬ０Ｏｏ𐊒𐊫𐐄𐐬𐓂𐓪𐔖𑓐𑢵𑣈𑣗𑣠𝐎𝐨𝑂𝑜𝑶𝒐𝒪𝓞𝓸𝔒𝔬𝕆𝕠𝕺𝖔𝖮𝗈𝗢𝗼𝘖𝘰𝙊𝙤𝙾𝚘𝚶𝛐𝛔𝛰𝜊𝜎𝜪𝝄𝝈𝝤𝝾𝞂𝞞𝞸𝞼𝟎𝟘𝟢𝟬𝟶𞸤𞹤𞺄🯰',
        '1Iil|ıƖǀɩɪ˛ͺΙιІіӀӏ׀וןا١۱ߊᎥᛁιℐℑℓℹⅈⅠⅰⅼ∣⍳⏽Ⲓⵏꓲꙇꭵﺍﺎ１Ｉｉｌ￨𐊊𐌉𐌠𑣃𖼨𝐈𝐢𝐥𝐼𝑖𝑙𝑰𝒊𝒍𝒾𝓁𝓘𝓲𝓵𝔦𝔩𝕀𝕚𝕝𝕴𝖎𝖑𝖨𝗂𝗅𝗜𝗶𝗹𝘐𝘪𝘭𝙄𝙞𝙡𝙸𝚒𝚕𝚤𝚰𝛊𝛪𝜄𝜤𝜾𝝞𝝸𝞘𝞲𝟏𝟙𝟣𝟭𝟷𞣇𞸀𞺀🯱',
        '2ƧϨᒿꙄꛯꝚ２𝟐𝟚𝟤𝟮𝟸🯲',
        '3ƷȜЗӠⳌꝪꞫ３𑣊𖼻𝈆𝟑𝟛𝟥𝟯𝟹🯳',
        '4Ꮞ４𑢯𝟒𝟜𝟦𝟰𝟺🯴',
        '5Ƽ５𑢻𝟓𝟝𝟧𝟱𝟻🯵',
        '6бᏮⳒ６𑣕𝟔𝟞𝟨𝟲𝟼🯶',
        '7７𐓒𑣆𝈒𝟕𝟟𝟩𝟳𝟽🯷',
        '8Ȣȣ৪੪ଃ８𐌚𝟖𝟠𝟪𝟴𝟾𞣋🯸',
        '9৭੧୨൭ⳊꝮ９𑢬𑣌𑣖𝟗𝟡𝟫𝟵𝟿🯹'
    ]
    cuda_available = torch.cuda.is_available()

    args = ClassificationArgs(eval_batch_size = 32, use_multiprocessing_for_evaluation=False)
    model = ClassificationModel('roberta', classify_model_path, num_labels=len(labels_list), use_cuda=cuda_available, args = args)

    qq_terms_origin = []
    predictions, raw_outputs = model.predict(terms_all_list)

    for index, term in enumerate(terms_all_list):
        if labels_list[predictions[index]] == 'qq':
            qq_terms_origin.append(term)

    qq_terms = []
    args = ClassificationArgs(eval_batch_size = 32, use_multiprocessing_for_evaluation=False)
    model = ClassificationModel('roberta', qq_succeed_path, use_cuda=cuda_available, args = args)
    predictions, raw_outputs = model.predict(qq_terms_origin)
    for index, term in enumerate(qq_terms_origin):
        if predictions[index] == 1:
            qq_terms.append(term)

    print(f'Finish contact classification, get qq term {len(qq_terms)}')

    for term in qq_terms:
        term_origin = term
        term = term.lower()
        term = term.replace('q', '')
        term = term.replace('-', '')
        term = term.replace('_', '')
        term = term.replace('—', '')
        term = term.replace('扣', '')
        for char in term:
            for simple_num, similar_num in enumerate(unicode_similar_nums):
                if char in similar_num:
                    term = term.replace(char, str(simple_num))
                    break

        compileX = re.compile(r"\d+")
        num_result = compileX.findall(term)
        for nums in num_result:
            if len(nums) >= 7 and len(nums) <= 12:
                qq_contact[nums] = term_origin
                break
    #-------------------------------------------------------------------------------------------------
    


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
qq_contact = {}
num = 0
index_term = 0

for item in terms_all:
    num += 1
    index_term += 1
    terms_all_list.append(item)
    if num >= 50000:
        print(f'Get {len(terms_all_list)} positive terms')
        get_qq_contact(terms_all_list, qq_contact)
        logging.info(f'Finished terms {index_term} of {len(terms_all)} for extracting qq contact, get {len(qq_contact)} qq contacts')
        num = 0
        terms_all_list = []


print(f'Get {len(terms_all_list)} positive terms')

get_qq_contact(terms_all_list, qq_contact)

print(f'Finish extract qq contact, get {len(qq_contact)}')
with open('data/qq_contact.txt', 'w', encoding='utf-8') as fp:
    for item in qq_contact:
        fp.write(str((item, qq_contact[item])))
        fp.write('\n')

