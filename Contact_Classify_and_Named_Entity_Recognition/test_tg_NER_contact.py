import numpy as np
import pandas as pd
from scipy.special import softmax
from sklearn.model_selection import train_test_split
import csv
from simpletransformers.ner import NERModel
import torch
import jieba
model_path = '/data/jlxue/RBSEO_NER_train_model'

with open("classified_contact.csv", mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    sentences = []
    sentences_raw = []
    for row in reader:
        if row[1] == 'telegram':
            seg = jieba.cut(row[0])
            sentence = ''
            for item in seg:
                sentence += item + ' '
            sentences_raw.append(row[0])
            sentences.append(sentence)

# Create a NERModel
labels = ['B-contact', 'I-contact', 'O']

cuda_available = torch.cuda.is_available()
model = NERModel(
    "roberta",
    model_path,
    labels=labels,
    use_cuda=cuda_available,
)

# # Predictions on arbitary text strings
predictions, raw_outputs = model.predict(sentences)

# print(predictions)

# # More detailed preditctions
# for n, (preds, outs) in enumerate(zip(predictions, raw_outputs)):
#     print("\n___________________________")
#     print("Sentence: ", sentences[n])
#     for pred, out in zip(preds, outs):
#         key = list(pred.keys())[0]
#         new_out = out[key]
#         preds = list(softmax(np.mean(new_out, axis=0)))
#         print(key, pred[key], preds[np.argmax(preds)], preds)

contact_extract = [['term', 'contact_1', 'contact_2', 'contact_3', 'contact_4']]
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
        print(result_index)
        for pred, out in zip(preds, outs):
            key = list(pred.keys())[0]
            new_out = out[key]
            preds = list(softmax(np.mean(new_out, axis=0)))
            print(key, pred[key], preds[np.argmax(preds)], preds)
    contact_extract.append(result)

with open('NERed_contact.csv', mode='w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerows(contact_extract)