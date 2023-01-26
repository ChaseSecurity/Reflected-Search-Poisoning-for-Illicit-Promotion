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

NER_model_path = '/data/jlxue/RBSEO_wechat_NER_train_model'
classify_model_path = '/data/jlxue/RBSEO_contact_classifier_train_model'

terms_with_wechat = set()
terms_extracted = set()

def numeric_num(term):
    cnt = 0
    for s in term:
        if s.isdecimal():
            cnt += 1
    return cnt


def postprocess_wechat(im:str):
    im = im.lower()
    im_split = im.split('-')
    im_final = ''
    for item in im_split:
        if numeric_num(item) >= 7:
            im_final = item
            break
        else:
            im_final += item
    im_final = re.sub(r'[^a-zA-Z0-9_]', '', im_final)
    im_final = im_final.replace('vx', '')
    im_final = im_final.replace('wechat', '')
    if numeric_num(im_final) >= 7:
        im_final = re.sub(r'[a-zA-Z_]', '', im_final)
    return im_final

def get_wechat_contact(terms_all_list, wechat_contact):
    unicode_similar_nums = [ 
        '0ΟοσОо０Օօסه٥ھ⓿ہە۵߀०০੦૦ଠ୦௦ం౦ಂ೦ംഠ൦ං๐໐ဝ၀ჿዐᴏᴑℴⲞⲟⵔ〇ꓳꬽﮦﮧﮨﮩﮪﮫﮬﮭﻩﻪﻫﻬ０Ｏｏ𐊒𐊫𐐄𐐬𐓂𐓪𐔖𑓐𑢵𑣈𑣗𑣠𝐎𝐨𝑂𝑜𝑶𝒐𝒪𝓞𝓸𝔒𝔬𝕆𝕠𝕺𝖔𝖮𝗈𝗢𝗼𝘖𝘰𝙊𝙤𝙾𝚘𝚶𝛐𝛔𝛰𝜊𝜎𝜪𝝄𝝈𝝤𝝾𝞂𝞞𝞸𝞼𝟎𝟘𝟢𝟬𝟶𞸤𞹤𞺄🯰',
        '1|ı⒈Ɩ①❶１ǀ➊ɩɪ˛ͺΙιІіӀӏ׀וןا١۱ߊᎥᛁιℐℑℓℹⅈⅠⅰⅼ∣⍳⏽Ⲓⵏꓲꙇꭵﺍﺎ１Ｉｉｌ￨𐊊𐌉𐌠𑣃𖼨𝐈𝐢𝐥𝐼𝑖𝑙𝑰𝒊𝒍𝒾𝓁𝓘𝓲𝓵𝔦𝔩𝕀𝕚𝕝𝕴𝖎𝖑𝖨𝗂𝗅𝗜𝗶𝗹𝘐𝘪𝘭𝙄𝙞𝙡𝙸𝚒𝚕𝚤𝚰𝛊𝛪𝜄𝜤𝜾𝝞𝝸𝞘𝞲𝟏𝟙𝟣𝟭𝟷𞣇𞸀𞺀🯱',
        '2ƧϨ⒉ᒿꙄ②ꛯ❷Ꝛ➋２𝟐𝟚𝟤𝟮𝟸🯲',
        '3ƷȜЗ③❸⒊ӠⳌꝪꞫ３➌𑣊𖼻𝈆𝟑𝟛𝟥𝟯𝟹🯳',
        '4Ꮞ④⒋４❹➍𑢯𝟒𝟜𝟦𝟰𝟺🯴',
        '5Ƽ⑤⒌❺５➎𑢻𝟓𝟝𝟧𝟱𝟻🯵',
        '6⑥бᏮ❻⒍➏❻６Ⳓ６𑣕𝟔𝟞𝟨𝟲𝟼🯶',
        '7⑦７❼⒎➐𐓒𑣆𝈒𝟕𝟟𝟩𝟳𝟽🯷',
        '8Ȣȣ⑧⒏８৪❽➑੪ଃ８𐌚𝟖𝟠𝟪𝟴𝟾𞣋🯸',
        '9৭੧⑨୨⒐൭ⳊꝮ➒９𑢬𑣌❾𑣖𝟗𝟡𝟫𝟵𝟿🯹'
    ]
    cuda_available = torch.cuda.is_available()

    args = ClassificationArgs(eval_batch_size = 32, use_multiprocessing_for_evaluation=False)
    model = ClassificationModel('roberta', classify_model_path, num_labels=len(labels_list), use_cuda=cuda_available, args = args)

    wechat_terms = []
    predictions, raw_outputs = model.predict(terms_all_list)

    for index, term in enumerate(terms_all_list):
        if labels_list[predictions[index]] == 'wechat':
            wechat_terms.append(term)

    print(f'Finish contact classification, get wechat term {len(wechat_terms)}')
    #-------------------------------------------------------------------------------------------------
    sentences = []
    sentences_raw = []
    for term in wechat_terms:
        term_raw = term
        for char in term:
            for simple_num, similar_num in enumerate(unicode_similar_nums):
                if char in similar_num:
                    term = term.replace(char, str(simple_num))
                    break
        term = term.replace('⑩', '10')
        term = term.replace('⒑', '10')
        term = term.replace('⒒', '11')
        term = term.replace('⒓', '12')
        term = term.replace('⒔', '13')
        term = term.replace('⒕', '14')
        term = term.replace('⒖', '15')
        term = term.replace('⒗', '16')
        term = term.replace('⒘', '17')
        term = term.replace('⒙', '18')
        term = term.replace('⒚', '19')
        term = term.replace('⒛', '20')
        term = term.replace('.', '')
        seg = jieba.cut(term)
        sentence = ''
        for s in seg:
            sentence += s + ' '
        # Token indices sequence length is longer than the specified maximum sequence length for this model (683 > 512). 
        # Running this sequence through the model will result in indexing errors
        if len(sentence) < 512:
            sentences_raw.append(term_raw)
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
        if result[1] != '' and len(result[1]) > 4:
            result[1] = postprocess_wechat(result[1])
            if result[1] not in wechat_contact.keys():
                wechat_contact[result[1]] = [sentences_raw[n], 1]
                terms_with_wechat.add(sentences_raw[n])
                terms_extracted.add((sentences_raw[n], result[1]))
            else:
                wechat_contact[result[1]][1] += 1
                terms_with_wechat.add(sentences_raw[n])
                terms_extracted.add((sentences_raw[n], result[1]))


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
data = []
#-------------------------------------------------------------------------------------------------
labels_list = ['website', 'wechat', 'qq', 'telegram', 'others','telephone']
labels_dict = {'website':0, 'wechat':1, 'qq':2, 'telegram':3, 'others':4, 'telephone':5}
terms_all_list = []
wechat_contact = {}
num = 0
index_term = 0

for item in terms_all:
    num += 1
    index_term += 1
    terms_all_list.append(item)
    if num >= 50000:
        print(f'Get {len(terms_all_list)} positive terms')
        get_wechat_contact(terms_all_list, wechat_contact)
        logging.info(f'Finished terms {index_term} of {len(terms_all)} for extracting wechat contact, get {len(wechat_contact)} wechat contacts')
        num = 0
        terms_all_list = []
        with open('data/wechat_contact.txt', 'w', encoding='utf-8') as fp:
            wechat_list = []
            for wechat in wechat_contact:
                wechat_list.append((wechat, wechat_contact[wechat][0], wechat_contact[wechat][1]))

            wechat_list.sort(key=lambda x: -x[2])
            for item in wechat_list:
                fp.write(str(item))
                fp.write('\n')


print(f'Get {len(terms_all_list)} positive terms')

get_wechat_contact(terms_all_list, wechat_contact)

print(f'Finish extract wechat contact, get {len(wechat_contact)}')
with open('data/wechat_contact.txt', 'w', encoding='utf-8') as fp:
    wechat_list = []
    for wechat in wechat_contact:
        wechat_list.append((wechat, wechat_contact[wechat][0], wechat_contact[wechat][1]))

    wechat_list.sort(key=lambda x: -x[2])
    for item in wechat_list:
        fp.write(str(item))
        fp.write('\n')

with open('data/terms_with_wechat.txt', 'w', encoding='utf-8') as fp:
    for item in terms_with_wechat:
        fp.write(item)
        fp.write('\n')

with open('data/terms_extracted_wechat.txt', 'w', encoding='utf-8') as fp:
    for item in terms_extracted:
        fp.write(str(item))
        fp.write('\n')