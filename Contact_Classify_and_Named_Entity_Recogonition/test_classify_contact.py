from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
from sklearn.metrics import f1_score,  accuracy_score
from sklearn.model_selection import train_test_split
import torch
import csv
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)
eval_num = 2000

model_path = '/data/jlxue/RBSEO_contact_classifier_train_model'

#--------------------------Read Classes---------------------------
labels_list = ['website', 'wechat', 'qq', 'telegram', 'others']
labels_dict = {'website':0, 'wechat':1, 'qq':2, 'telegram':3, 'others':4}

logging.info(f"Finish getting labels, get {len(labels_list)} classes. ")

#-------------------------------Read Terms------------------------------
with open("Reflected_Blackhat_SEO_terms_for_labeling - main.csv", mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    all_data = []
    for row in reader:
        all_data.append(row)

unlabeled_data = []
cnt = 0
for item in all_data:
    if item[1] == '':
        unlabeled_data.append(item[0])
        cnt +=1
    if cnt >= eval_num:
        break

logging.info(f"Finish getting terms, get {len(unlabeled_data)} unlabeled data. ")

#------------------------------Classify---------------------------
cuda_available = torch.cuda.is_available()
model = ClassificationModel('roberta', model_path, num_labels=len(labels_list), use_cuda=cuda_available)

classified_terms = []
predictions, raw_outputs = model.predict(unlabeled_data)
for index, term in enumerate(unlabeled_data):
    classified_terms.append([term, labels_list[predictions[index]]])

with open('classified_contact.csv', mode='w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerows(classified_terms)
pass