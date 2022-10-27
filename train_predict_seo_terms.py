"""
Follow tutorials listed below
  https://github.com/ThilinaRajapakse/simpletransformers
"""

from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
import ast
import sys
import sklearn
from sklearn.model_selection import train_test_split
import torch
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

positive_cases = [
    (
        ast.literal_eval(line.strip())[0],
        1
    )
    for line in open("./positive_data.txt")
]
negative_cases = [
    (
        ast.literal_eval(line.strip())[0],
        0
    )
    for line in open("./negative_data.txt")
]
# TODO deduplicate
logging.info(f"Loaded {len(positive_cases)}")
logging.info(f"Loaded {len(negative_cases)}")

samples = negative_cases + positive_cases

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

sample_df = pd.DataFrame(samples)
sample_df.columns = ["text", "labels"]
train_df, eval_df = train_test_split(sample_df, test_size=0.2)

# Optional model configuration
cuda_available = torch.cuda.is_available()
model_args = ClassificationArgs(num_train_epochs=1)

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
result, model_outputs, wrong_predictions = model.eval_model(eval_df)

# Make predictions with the model
# predictions, raw_outputs = model.predict(["Sam was a Wizard"])
