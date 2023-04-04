# train_classify_telegram_messages.py

"""
Follow tutorials listed below
  https://github.com/ThilinaRajapakse/simpletransformers
"""
version = 'v5'
output_path = f'/data/sangyiwu/RBSEO_classifier_train_model/{version}'

from simpletransformers.classification import MultiLabelClassificationModel
import pandas as pd
import logging
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import torch
import csv
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)


#--------------------------Read Classes---------------------------
labels_list = []
labels_dict = {}
with open(f'./{version}/labels.txt', 'r', encoding='utf-8') as fp:
    reader = fp.readlines()
for index, item in enumerate(reader):
    label = item[:-1]
    labels_dict[label] = index
    labels_list.append(label)

logging.info(f"Finish getting labels, get {len(labels_list)} classes. ")

#---------------------------------Get Train Set---------------------------
with open(f'./{version}/labeled_messages.csv', mode='r', encoding='utf-8') as fp:
    reader = csv.reader(fp)
    next(reader)
    samples = []
    for row in reader:
        one_data = []
        one_data.append(row[2])
        one_data_label = [0 for i in range(len(labels_list))]
        if row[4] != '':
            one_data_label[labels_dict[row[4]]] = 1
        if row[5] != '':
            one_data_label[labels_dict[row[5]]] = 1
        if row[6] != '':
            one_data_label[labels_dict[row[6]]] = 1
        if row[7] != '':
            one_data_label[labels_dict[row[7]]] = 1
        samples.append([row[2], one_data_label])

logging.info(f"Loaded {len(samples)} samples.")

sample_df = pd.DataFrame(samples)
sample_df.columns = ["text", "labels"]
train_df, eval_df = train_test_split(sample_df, test_size=0.2, random_state=2)

# Optional model configuration
cuda_available = torch.cuda.is_available()

# Create a ClassificationModel
model = MultiLabelClassificationModel(
    "bert",
    "bert-base-multilingual-cased",
    use_cuda=cuda_available,
    args={
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "num_train_epochs": 50,
        "output_dir": output_path
    },
    num_labels=len(labels_list),
)

def precision_score_multilabel_weighted(y_true, y_pred):
    y_pred = y_pred.round()
    return precision_score(y_true, y_pred, average='weighted')
def precision_score_multilabel_micro(y_true, y_pred):
    y_pred = y_pred.round()
    return precision_score(y_true, y_pred, average='micro')
def precision_score_multilabel_macro(y_true, y_pred):
    y_pred = y_pred.round()
    return precision_score(y_true, y_pred, average='macro')
def precision_score_multilabel_samples(y_true, y_pred):
    y_pred = y_pred.round()
    return precision_score(y_true, y_pred, average='samples')

def recall_score_multilabel_weighted(y_true, y_pred):
    y_pred = y_pred.round()
    return recall_score(y_true, y_pred, average='weighted')
def recall_score_multilabel_micro(y_true, y_pred):
    y_pred = y_pred.round()
    return recall_score(y_true, y_pred, average='micro')
def recall_score_multilabel_macro(y_true, y_pred):
    y_pred = y_pred.round()
    return recall_score(y_true, y_pred, average='macro')
def recall_score_multilabel_samples(y_true, y_pred):
    y_pred = y_pred.round()
    return recall_score(y_true, y_pred, average='samples')

def f1_score_multilabel_weighted(y_true, y_pred):
    y_pred = y_pred.round()
    return f1_score(y_true, y_pred, average='weighted')
def f1_score_multilabel_micro(y_true, y_pred):
    y_pred = y_pred.round()
    return f1_score(y_true, y_pred, average='micro')
def f1_score_multilabel_macro(y_true, y_pred):
    y_pred = y_pred.round()
    return f1_score(y_true, y_pred, average='macro')
def f1_score_multilabel_samples(y_true, y_pred):
    y_pred = y_pred.round()
    return f1_score(y_true, y_pred, average='samples')

def accuracy_score_multilabel(y_true, y_pred):
    y_pred = y_pred.round()
    return accuracy_score(y_true, y_pred)

def classification_report_multilabel(y_true, y_pred):
    y_pred = y_pred.round()
    return classification_report(y_true, y_pred, target_names=labels_list)

# Train the model
model.train_model(
    train_df, 
    eval_df, 
    accuracy = accuracy_score_multilabel,
    precision_micro = precision_score_multilabel_micro, 
    precision_macro = precision_score_multilabel_macro, 
    precision_weighted = precision_score_multilabel_weighted, 
    precision_samples = precision_score_multilabel_samples, 
    recall_micro = recall_score_multilabel_micro, 
    recall_macro = recall_score_multilabel_macro, 
    recall_weighted = recall_score_multilabel_weighted, 
    recall_samples = recall_score_multilabel_samples, 
    f1_micro = f1_score_multilabel_micro,
    f1_macro = f1_score_multilabel_macro,
    f1_weighted = f1_score_multilabel_weighted,
    f1_samples = f1_score_multilabel_samples,
    classification_report = classification_report_multilabel
)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(
    eval_df, 
    accuracy = accuracy_score_multilabel,
    precision_micro = precision_score_multilabel_micro, 
    precision_macro = precision_score_multilabel_macro, 
    precision_weighted = precision_score_multilabel_weighted, 
    precision_samples = precision_score_multilabel_samples, 
    recall_micro = recall_score_multilabel_micro, 
    recall_macro = recall_score_multilabel_macro, 
    recall_weighted = recall_score_multilabel_weighted, 
    recall_samples = recall_score_multilabel_samples, 
    f1_micro = f1_score_multilabel_micro,
    f1_macro = f1_score_multilabel_macro,
    f1_weighted = f1_score_multilabel_weighted,
    f1_samples = f1_score_multilabel_samples,
    classification_report = classification_report_multilabel
)

# Export the wrong predictions
wrong_predictions_to_save = []
for wp in wrong_predictions:
    idx = wp.guid
    prediction = model_outputs[idx]
    wrong_predictions_to_save.append([wp.text_a, prediction, wp.label])

with open(f'./{version}/wrong_predictions.csv', 'w', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['text', 'prediction', 'label'])
    csvwriter.writerows(wrong_predictions_to_save)
