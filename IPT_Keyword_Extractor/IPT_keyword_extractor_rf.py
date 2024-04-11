import logging
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from util import *
import pickle
import warnings
import argparse
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--model_path', type=str, default='', required=True, help='The trained model output directory')
parser.add_argument('--gt_dir', type=str, default='./groundtruth', help='The ground truth dataset directory')
args = parser.parse_args()

model_dir = args.model_path
ground_truth_dir = args.gt_dir

positive_cases = [
    (
        line.strip(),
        1
    )
    for line in open(f"{ground_truth_dir}/keywords_positive.txt", encoding='utf-8')
]
negative_cases = [
    (
        line.strip(),
        0
    )
    for line in open(f"{ground_truth_dir}/keywords_negative.txt", encoding='utf-8')
]
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
recall = metrics.recall_score(test_labels, predicts)
precision = metrics.precision_score(test_labels, predicts)
f1 = metrics.f1_score(test_labels, predicts)
logging.info(f"Random Forest, Recall {recall}, precision {precision}, f1 {f1}")
with open(f'{model_dir}/random_forest_model_keywords.pickle', 'wb') as f:
    pickle.dump(clf, f)
