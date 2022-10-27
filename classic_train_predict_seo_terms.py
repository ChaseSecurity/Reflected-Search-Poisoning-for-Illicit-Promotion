import pandas as pd
import logging
import ast
import sklearn
from sklearn import tree, metrics
from sklearn.model_selection import train_test_split
import torch
logging.basicConfig(level=logging.INFO)
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
train_samples, test_samples = train_test_split(samples, test_size=0.2)

def feature_extract(sample):
    features = []
    # length in in characters
    features.append(len(sample))
    # if [, ],【 】pass
    if "[" in sample and "]" in sample:
        features.append(1)
    else:
        features.append(0)
    if "【" in sample and "】" in sample:
        features.append(1)
    else:
        features.append(0)
    # url number
    # TODO add the following features
    # url number
    # number of non alphanumeric characters
    # number of numberic characters
    # longest number string
    return features

# TODO, try different classific classification algorithms, random forest, svm, decision tree, GBDT, etc
train_features = [
    feature_extract(sample)
    for sample,label in train_samples
]
train_labels = [
    label
    for sample,label in train_samples
]
# TODO tune the parameters
clf = tree.DecisionTreeClassifier()
clf.fit(train_features, train_labels)
test_features = [
    feature_extract(sample)
    for sample, label in test_samples
]
test_labels = [
    label
    for sample, label in test_samples
]
predicts = clf.predict(test_features)
recall = metrics.recall_score(test_labels, predicts)
precision = metrics.precision_score(test_labels, predicts)
f1 = metrics.f1_score(test_labels, predicts)
logging.info(f"Recall {recall}, precision {precision}, f1 {f1}")
