import numpy as np
import pandas as pd
from scipy.special import softmax
from sklearn.model_selection import train_test_split
import csv
from simpletransformers.ner import NERModel
output_path = '/data/jlxue/RBSEO_wechat_NER_train_model'

with open("wechat_NER_for_labeling.csv", mode="r", encoding="utf-8") as fp:
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

# Creating train_df  and eval_df for demonstration
sample_df = pd.DataFrame(samples)
sample_df.columns = ["sentence_id", "words", "labels"]
train_df, eval_df = train_test_split(sample_df, test_size=0.2)

# Create a NERModel
labels = ['B-contact', 'I-contact', 'O']
model = NERModel(
    "roberta",
    "roberta-base",
    labels=labels,
    args={
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "num_train_epochs": 25,
        "output_dir": output_path
    },
)

# # Train the model
model.train_model(train_df)

# # Evaluate the model
result, model_outputs, predictions = model.eval_model(eval_df)


# # Predictions on arbitary text strings
# sentences = ["Some arbitary sentence", "Simple Transformers sentence"]
# predictions, raw_outputs = model.predict(sentences)

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