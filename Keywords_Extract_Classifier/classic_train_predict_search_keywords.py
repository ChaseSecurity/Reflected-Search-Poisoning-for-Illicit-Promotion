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
import torch
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
# TODO deduplicate
logging.info(f"Loaded {len(positive_cases)}")
logging.info(f"Loaded {len(negative_cases)}")

samples = negative_cases + positive_cases
train_samples, test_samples = train_test_split(samples, test_size=0.2)

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
# TODO tune the parameters

# TODO, try different classific classification algorithms, random forest, svm, decision tree, GBDT, etc
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
logging.info(f"Decision Tree, Recall {recall}, precision {precision}, f1 {f1}")

#TODO adaboost
clf = AdaBoostClassifier(base_estimator=None, n_estimators=100, learning_rate=1.0, algorithm='SAMME.R', random_state=10)
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
logging.info(f"Ada Boost, Recall {recall}, precision {precision}, f1 {f1}")
# with open('adaboost_model.pickle', 'wb') as f:
#     pickle.dump(clf, f)

#TODO random forest
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
recall = metrics.recall_score(test_labels, predicts)
precision = metrics.precision_score(test_labels, predicts)
f1 = metrics.f1_score(test_labels, predicts)
logging.info(f"Random Forest, Recall {recall}, precision {precision}, f1 {f1}")
with open('random_forest_model_keywords.pickle', 'wb') as f:
    pickle.dump(clf, f)

#TODO SVM
clf = LinearSVC(penalty='l2', loss='squared_hinge', dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True, intercept_scaling=1, class_weight=None, verbose=0, random_state=10, max_iter=10000)
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
logging.info(f"SVM, Recall {recall}, precision {precision}, f1 {f1}")