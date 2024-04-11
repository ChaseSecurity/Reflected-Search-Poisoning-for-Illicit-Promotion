import pandas as pd
import csv
from simpletransformers.ner import NERModel
import torch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--im', type=str, default='', required=True, help='IM type (telegram / wechat)')
parser.add_argument('--model_path', type=str, default='', required=True, help='The trained model output directory')
parser.add_argument('--gt_dir', type=str, default='./groundtruth', help='The ground truth dataset directory')
args = parser.parse_args()

model_dir = args.model_path
ground_truth_dir = args.gt_dir

if args.im == 'telegram':
    output_path = f"{model_dir}/telegram_NER_model"
    train_path = f"{ground_truth_dir}/contact_NER_for_labeling_telegram.csv"
    eval_path = f"{ground_truth_dir}/telegram_NER_for_eval.csv"
elif args.im == 'wechat':
    output_path = f"{model_dir}/wechat_NER_model"
    train_path = f"{ground_truth_dir}/contact_NER_for_labeling_wechat.csv"
    eval_path = f"{ground_truth_dir}/wechat_NER_for_eval.csv"
else:
    raise ValueError('Please choose IM (wechat or telegram)')

with open(train_path, mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    samples = []
    for row in reader:
        sentence_num = eval(row[0])
        wd = row[1]
        if row[2] == '':
            label = 'O'
        else:
            label = row[2]
        samples.append([sentence_num, wd, label])

with open(eval_path, mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    eval_samples = []
    for row in reader:
        sentence_num = eval(row[0])
        wd = row[1]
        if row[2] == '':
            label = 'O'
        else:
            label = row[2]
        eval_samples.append([sentence_num, wd, label])

# Creating train_df  and eval_df for demonstration
sample_df = pd.DataFrame(samples)
sample_df.columns = ["sentence_id", "words", "labels"]

eval_sample_df = pd.DataFrame(eval_samples)
eval_sample_df.columns = ["sentence_id", "words", "labels"]

# Create a NERModel
cuda_available = torch.cuda.is_available()

labels = ['B-contact', 'I-contact', 'O']
model = NERModel(
    "roberta",
    "roberta-base",
    labels=labels,
    use_cuda=cuda_available,
    args={
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "num_train_epochs": 15,
        "output_dir": output_path
    },
)

# Train the model
model.train_model(sample_df)
# Evaluate the model
result, model_outputs, predictions = model.eval_model(eval_sample_df)