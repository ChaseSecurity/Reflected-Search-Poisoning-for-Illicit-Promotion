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
from util import *

def Predict_With_Model(model, terms):
    def non_alphanumeric_num(term):
        cnt = 0
        for s in term:
            if (not s.isalpha()) and (not s.isdecimal()):
                cnt += 1
        return cnt

    def numeric_num(term):
        cnt = 0
        for s in term:
            if s.isdecimal():
                cnt += 1
        return cnt

    def patterns_num(term):
        patterns = ['微信', 'q微', '扣微', '微', '薇', '扣扣', 'qq',\
                    'com', 'fun', 'cc', 'hash', 'tg', 'telegram', \
                    '飞机', '@']
        cnt = 0
        for p in patterns:
            if p in term.lower():
                cnt += 1
        return cnt

    def brackets_num(term):
        brackets_num = ['[', ']', '【', '】', '(', ')', '（',\
                    '）', '『', '』', '《', '》', '<', \
                    '>', '☀️', '👉']
        cnt = 0
        for p in brackets_num:
            if p in term:
                cnt += 1
        return cnt

    def has_suffix(term):
        suffix = ['.html', '.shtml', '.htm', '.php', '.pdf', '.jpg', '.jpeg', '.png', '.xlsx', '.doxx', '.pptx', '.xml']
        for s in suffix:
            if s in term:
                return 1
        return 0

    def url_num(term):
        url_pattern = r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?'
        return len(re.findall(url_pattern, term))

    def feature_extract(sample):
        features = []
        # length in in characters
        features.append(len(sample))
        # number of brackets
        features.append(brackets_num(sample))
        # number of urls in term
        features.append(url_num(sample))
        # number of non alphanumeric characters
        features.append(non_alphanumeric_num(sample))
        # number of numberic characters
        features.append(numeric_num(sample))
        # num of some contact info patterns
        features.append(patterns_num(sample))
        # if some suffix of web file in sample
        features.append(has_suffix(sample))
        #TODO more features
        return features
    features = [
        feature_extract(sample)
        for sample in terms
    ]
    return model.predict(features)


def Predict_Keywords_With_Model(model, keywords):
    def non_alphanumeric_num(term):
        cnt = 0
        for s in term:
            if (not s.isalpha()) and (not s.isdecimal()):
                cnt += 1
        return cnt

    def numeric_num(term):
        cnt = 0
        for s in term:
            if s.isdecimal():
                cnt += 1
        return cnt

    def patterns_num(term):
        patterns = ['微信', 'q微', '扣微', '微', '薇', '扣扣', 'qq',\
                    'com', 'fun', 'cc', 'hash', 'tg', 'telegram', \
                    '飞机', '@']
        cnt = 0
        for p in patterns:
            if p in term.lower():
                cnt += 1
        return cnt

    def brackets_num(term):
        brackets_num = ['[', ']', '【', '】', '(', ')', '（',\
                    '）', '『', '』', '《', '》', '<', \
                    '>', '☀️', '👉']
        cnt = 0
        for p in brackets_num:
            if p in term:
                cnt += 1
        return cnt

    def has_suffix(term):
        suffix = ['.html', '.htm', '.php', '.pdf', '.jpg', '.jpeg', '.png']
        for s in suffix:
            if s in term:
                return 1
        return 0

    def url_num(term):
        url_pattern = r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?'
        return len(re.findall(url_pattern, term))

    def punctuation_num(term):
        patterns =  ['.', ':', '：', '·', 'ͺ', '-']
        cnt = 0
        for p in patterns:
            if p in term.lower():
                cnt += 1
        return cnt
    
    def alphanumeric_num(term):
        cnt = 0
        for s in term:
            if s.isalpha() or s.isdecimal():
                cnt += 1
        return cnt

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

    features = [
        feature_extract(sample)
        for sample in keywords
    ]
    return model.predict(features)