from simpletransformers.classification import MultiModalClassificationModel
import logging
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, classification_report
import torch

output_dir = "/data/sangyiwu/RBSEO_Cybercrime_Website_Classifier"

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Read Classes
labels_list = []
with open('labels.txt', 'r', encoding='utf-8') as fp:
    reader = fp.readlines()
for index, item in enumerate(reader):
    label = item[:-1]
    labels_list.append(label)

logging.info(f"Finish getting labels, get {len(labels_list)} classes.")

# Get Train Set
with open('labeled_samples.csv', mode='r', encoding='utf-8') as fp:
    reader = csv.reader(fp)
    samples = []
    headers = next(reader)
    for row in reader:
        samples.append([row[0][22:], row[2], row[3]])

logging.info(f"Loaded {len(samples)} samples.")

sample_df = pd.DataFrame(samples)
sample_df.columns = ["images", "text", "labels"]
train_df, eval_df = train_test_split(sample_df, test_size=0.25, random_state=1)
train_df.to_csv("train_df.csv", index=False)
eval_df.to_csv("eval_df.csv", index=False)

# Create a ClassificationModel
cuda_available = torch.cuda.is_available()

model = MultiModalClassificationModel(
    "bert",
    "bert-base-multilingual-uncased",
    use_cuda=cuda_available,
    args={
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "num_train_epochs": 50,
        "fp16": False,
        "train_batch_size": 8,
        "eval_batch_size": 8,
        "output_dir": output_dir,
        # "evaluate_during_training": True,
        # "best_model_dir": f"{output_dir}/best"
    },
    label_list=labels_list,
)

def precision_score_multimodal(y_true, y_pred):
    y_pred = y_pred.round()
    return precision_score(y_true, y_pred, average='weighted')

def recall_score_multimodal(y_true, y_pred):
    y_pred = y_pred.round()
    return recall_score(y_true, y_pred, average='weighted')

def f1_score_multimodal(y_true, y_pred):
    y_pred = y_pred.round()
    return f1_score(y_true, y_pred, average='weighted')

def acc_score_multimodal(y_true, y_pred):
    y_pred = y_pred.round()
    return accuracy_score(y_true, y_pred, normalize=True)

def classification_report_multimodal(y_true, y_pred):
    y_pred = y_pred.round()
    return classification_report(y_true, y_pred, target_names=labels_list)

# Train the model
model.config.use_return_dict = True
model.train_model(
    train_df,
    eval_data = eval_df,
    image_path="/data/sangyiwu/",
    precision = precision_score_multimodal, 
    recall = recall_score_multimodal, 
    f1 = f1_score_multimodal,
    acc = acc_score_multimodal,
    classification = classification_report_multimodal,
)

# Evaluate the model
result, model_outputs = model.eval_model(
    eval_df, 
    image_path="/data/sangyiwu/",
    precision = precision_score_multimodal, 
    recall = recall_score_multimodal, 
    f1 = f1_score_multimodal,
    acc = acc_score_multimodal,
    classification = classification_report_multimodal,
)

with open("eval_outputs.csv", "w", encoding="utf-8", newline="") as fp:
    csvwriter = csv.writer(fp)
    csvwriter.writerow(
        ['(Fake) Certificate & Account & Merchandise',
        'Drug',
        'Financial related',
        'Gambling',
        'Benign',
        'Hacker & Crime',
        'Sales & Advertisement',
        'SEO',
        'Sex & Porn',
        'Unknown',
        'Redirection Page',
        'Domain Expired'])
    csvwriter.writerows(model_outputs)
