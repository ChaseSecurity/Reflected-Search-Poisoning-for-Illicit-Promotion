from random import sample
import pandas as pd
import logging
import ast
import sklearn
from sklearn import tree, metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC
# import torch
from util import *
import pickle
import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)
positive_cases = [
    (
        line.strip(),
        1
    )
    for line in open("./keywords_positive.txt", encoding='utf-8')
]
negative_cases = [
    (
        line.strip(),
        0
    )
    for line in open("./keywords_negative.txt", encoding='utf-8')
]
positive_tests = [
    (
        line.strip(),
        1
    )
    for line in open("./positive_keywords_for_eval.txt", encoding='utf-8')
]
negative_tests = [
    (
        line.strip(),
        0
    )
    for line in open("./negative_keywords_for_eval.txt", encoding='utf-8')
]
# TODO deduplicate
logging.info(f"Loaded {len(positive_cases)}")
logging.info(f"Loaded {len(negative_cases)}")

train_samples = negative_cases + positive_cases
test_samples = positive_tests + negative_tests

def feature_extract(sample):
    features = []
    # length in characters
    features.append(len(sample))
    # number of urls in term
    features.append(url_num(sample))
    # number of non alphanumeric characters
    features.append(non_alphanumeric_num(sample))
    # number of alphanumeric characters
    features.append(alphanumeric_num(sample))
    # number of numberic characters
    features.append(numeric_num(sample))
    # num of some contact info patterns
    features.append(patterns_num(sample))
    # Number of some common punctuation marks
    features.append(punctuation_num(sample))
    # if some suffix of web file in sample
    features.append(has_suffix(sample))
    #TODO more features
    return features

train_features = [
    feature_extract(sample)
    for sample,label in train_samples
]
train_labels = [
    label
    for sample,label in train_samples
]

clf = RandomForestClassifier(class_weight='balanced', random_state=10)
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

cm = metrics.confusion_matrix(test_labels, predicts)
# [[TN  FP]
#  [FN  TP]]
TN, FP, FN, TP = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
print(f'TP = {TP}, FN = {FN}, FP = {FP}, TN = {TN}')
print(f'Precision = {TP / (TP + FP)}, Recall = {TP / (TP + FN)}')