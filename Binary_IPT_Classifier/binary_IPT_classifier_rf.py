import logging
import ast
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from util import *
import pickle
import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)

# TODO: fill filepath
ground_truth_dir = ''
model_dir = ''

positive_cases = [
    (
        ast.literal_eval(line.strip())[0],
        1
    )
    for line in open(f"{ground_truth_dir}/positive_data.txt", encoding='utf-8')
]
negative_cases = [
    (
        ast.literal_eval(line.strip())[0],
        0
    )
    for line in open(f"{ground_truth_dir}/negative_data.txt", encoding='utf-8')
]
logging.info(f"Loaded {len(positive_cases)} Positive.")
logging.info(f"Loaded {len(negative_cases)} Negative.")

samples = negative_cases + positive_cases
train_samples, test_samples = train_test_split(samples, test_size=0.2, random_state=1)

def feature_extract(sample):
    features = []
    # length in characters
    features.append(len(sample))
    # number of brackets
    features.append(brackets_num(sample))
    # number of urls in term
    features.append(url_num(sample))
    # number of emojis
    features.append(emoji_num(sample))
    # number of unicode symbols
    features.append(unicodesymbol_num(sample))
    # number of numberic characters
    features.append(numeric_num(sample))
    # num of some contact info patterns
    features.append(patterns_num(sample))
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

clf = RandomForestClassifier(
    n_estimators=91,
    max_features=1,
    oob_score=True,
    class_weight='balanced', 
    random_state=10
    )
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
accuracy = metrics.accuracy_score(test_labels, predicts)
recall = metrics.recall_score(test_labels, predicts)
precision = metrics.precision_score(test_labels, predicts)
f1 = metrics.f1_score(test_labels, predicts)
mcc = metrics.matthews_corrcoef(test_labels, predicts)
logging.info(f"Random Forest, Recall {recall}, precision {precision}, f1 {f1}, mcc {mcc}, acc {accuracy}")
with open(f'{model_dir}/random_forest_model_binaryIPT.pickle', 'wb') as f:
    pickle.dump(clf, f)
