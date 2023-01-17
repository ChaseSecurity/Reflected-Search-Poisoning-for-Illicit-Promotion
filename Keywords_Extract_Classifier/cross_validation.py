import random
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
import numpy as np
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
# TODO deduplicate
logging.info(f"Loaded {len(positive_cases)}")
logging.info(f"Loaded {len(negative_cases)}")

samples = negative_cases + positive_cases

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

sample_features = [
    feature_extract(sample)
    for sample,label in samples
]
sample_labels = [
    label
    for sample,label in samples
]
sample_features = np.array(sample_features)
sample_labels = np.array(sample_labels)

from sklearn.model_selection import KFold
kf = KFold(n_splits=10, shuffle=True, random_state=True)
TP_total, FN_total, FP_total, TN_total = 0, 0, 0, 0

for train_i, test_i in kf.split(sample_features):
    train_features, train_labels = sample_features[train_i], sample_labels[train_i]
    test_features, test_labels = sample_features[test_i], sample_labels[test_i]
    clf = RandomForestClassifier(class_weight='balanced', random_state=10)
    clf.fit(train_features, train_labels)
    predicts = clf.predict(test_features)
    cm = metrics.confusion_matrix(test_labels, predicts)
    # [[TN  FP]
    #  [FN  TP]]
    TN, FP, FN, TP = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
    TP_total += TP
    FN_total += FN
    FP_total += FP
    TN_total += TN


print(f'TP = {TP_total}, FN = {FN_total}, FP = {FP_total}, TN = {TN_total}')
print(f'Precision = {TP_total / (TP_total + FP_total)}, Recall = {TP_total / (TP_total + FN_total)}')