import csv
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
from sklearn.metrics import f1_score,  accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
import torch
import csv
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

output_path = '/data/jlxue/qq_succeed_classifier_model'

with open('qq_succeed_label.csv', 'r', encoding='utf-8', newline='') as fp:
    reader = csv.reader(fp)
    samples = []
    for row in reader:
        if row[1] == '1':
            samples.append([row[0], 1])
        else:
            samples.append([row[0], 0])

sample_df = pd.DataFrame(samples)
sample_df.columns = ["text", "labels"]
train_df, eval_df = train_test_split(sample_df, test_size=0.2)

cuda_available = torch.cuda.is_available()
model_args = ClassificationArgs(num_train_epochs=20, overwrite_output_dir=True, output_dir=output_path)

# Create a ClassificationModel
model = ClassificationModel(
    "roberta",
    "roberta-base",
    use_cuda=cuda_available,
    args=model_args,
)

# Train the model
model.train_model(train_df)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df, f1=f1_score, acc=accuracy_score, \
    precision = precision_score, recall = recall_score)