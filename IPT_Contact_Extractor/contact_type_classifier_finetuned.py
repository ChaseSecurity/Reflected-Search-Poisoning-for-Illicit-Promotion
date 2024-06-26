"""
Follow tutorials listed below
  https://github.com/ThilinaRajapakse/simpletransformers
"""
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
from sklearn.metrics import f1_score,  accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
import torch
import csv
import argparse

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

parser = argparse.ArgumentParser()
parser.add_argument('--model_path', type=str, default='', required=True, help='The trained model output directory')
parser.add_argument('--gt_dir', type=str, default='./groundtruth', help='The ground truth dataset directory')
args = parser.parse_args()

model_dir = args.model_path
ground_truth_dir = args.gt_dir


# Read Classes
labels_list = ['website', 'wechat', 'qq', 'telegram', 'others','telephone']
labels_dict = {'website':0, 'wechat':1, 'qq':2, 'telegram':3, 'others':4, 'telephone':5}
logging.info(f"Finish getting labels, get {len(labels_list)} classes. ")

# Get Train Set
with open(f"{ground_truth_dir}/labeled_contact_type.csv", mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    samples = []
    for row in reader:
        samples.append((row[0], labels_dict[row[1].lower()]))
logging.info(f"Loaded {len(samples)}")


transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

sample_df = pd.DataFrame(samples)
sample_df.columns = ["text", "labels"]
train_df, eval_df = train_test_split(sample_df, test_size=0.05)

# Optional model configuration
cuda_available = torch.cuda.is_available()
model_args = ClassificationArgs(num_train_epochs=30, overwrite_output_dir=True, output_dir=model_dir)

# Create a ClassificationModel
model = ClassificationModel(
    "roberta",
    "roberta-base",
    use_cuda=cuda_available,
    args=model_args,
    num_labels=len(labels_list),
)

# Train the model
def f1_multiclass(labels, preds):
    return f1_score(labels, preds, average='micro')

def precision_score_multiclass(y_true, y_pred):
    return precision_score(y_true, y_pred, average='micro')

def recall_score_multiclass(y_true, y_pred):
    return recall_score(y_true, y_pred, average='micro')

model.train_model(train_df, eval_df = eval_df, f1=f1_multiclass, acc=accuracy_score, precision = precision_score_multiclass, recall = recall_score_multiclass)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df, f1=f1_multiclass, acc=accuracy_score, \
    precision = precision_score_multiclass, recall = recall_score_multiclass)
