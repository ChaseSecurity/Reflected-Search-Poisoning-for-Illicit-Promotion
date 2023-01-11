"""
Follow tutorials listed below
  https://github.com/ThilinaRajapakse/simpletransformers
"""

output_path = '/data/jlxue/RBSEO_classifier_train_model'

from simpletransformers.classification import MultiLabelClassificationModel
import pandas as pd
import logging
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
import torch
import csv
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)


#--------------------------Read Classes---------------------------
labels_list = []
labels_dict = {}
with open('labels.txt', 'r', encoding='utf-8') as fp:
    reader = fp.readlines()
for index, item in enumerate(reader):
    label = item[:-1]
    labels_dict[label] = index
    labels_list.append(label)

logging.info(f"Finish getting labels, get {len(labels_list)} classes. ")

#---------------------------------Get Train Set---------------------------
with open("labeled_terms.csv", mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    samples = []
    for row in reader:
        one_data = []
        one_data.append(row[0])
        one_data_label = [0 for i in range(len(labels_list))]
        if row[1] != '':
            one_data_label[labels_dict[row[1]]] = 1
        if row[2] != '':
            one_data_label[labels_dict[row[2]]] = 1
        if row[3] != '':
            one_data_label[labels_dict[row[3]]] = 1
        if row[4] != '':
            one_data_label[labels_dict[row[4]]] = 1
        samples.append([row[0], one_data_label])

logging.info(f"Loaded {len(samples)}")

sample_df = pd.DataFrame(samples)
sample_df.columns = ["text", "labels"]
train_df, eval_df = train_test_split(sample_df, test_size=0.2)

# Optional model configuration
cuda_available = torch.cuda.is_available()

# Create a ClassificationModel
model = MultiLabelClassificationModel(
    "roberta",
    "roberta-base",
    use_cuda=cuda_available,
    args={
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "num_train_epochs": 50,
        "output_dir": output_path
    },
    num_labels=len(labels_list),
)

def precision_score_multilabel(y_true, y_pred):
    y_pred = y_pred.round()
    return precision_score(y_true, y_pred, average='weighted')

def recall_score_multilabel(y_true, y_pred):
    y_pred = y_pred.round()
    return recall_score(y_true, y_pred, average='weighted')

def f1_score_multilabel(y_true, y_pred):
    y_pred = y_pred.round()
    return f1_score(y_true, y_pred, average='weighted')

# Train the model
model.train_model(train_df, eval_df, precision = precision_score_multilabel, recall = recall_score_multilabel, f1 = f1_score_multilabel)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df, precision = precision_score_multilabel, recall = recall_score_multilabel, f1 = f1_score_multilabel)


# Make predictions with the model
# predictions, raw_outputs = model.predict(["Sam was a Wizard"])
