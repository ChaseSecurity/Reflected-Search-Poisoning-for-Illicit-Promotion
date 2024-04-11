# Multi-label IPT Classifier

By fine tuning the multilingual BERT model `bert-base-multilingual-cased`, we build this classifier to profile what categories of services/goods an IPT is intended to promote. 

It takes an IPT as the input and then classifies it as either a harmless 'Benign' category or one or more of the 14 illicit services/goods:

| Benign                         |
|------------------------------- |
| Illegal Sex                    |
| Gambling                       |
| Illegal Surrogacy              |
| Black Hat SEO & Advertisement  |
| Fake Certificate               |
| Fake Account                   |
| Illegal Drug Sales             |
| Illegal Weapon Sales           |
| Data Theft                     |
| Hacking Service                |
| Money Laundering               |
| Counterfeit Goods              |
| Financial Fraud                |
| Others                         |

## Usage

```shell
$ python multilabel_IPT_classifier_finetuned.py -h
usage: multilabel_IPT_classifier_finetuned.py [-h] --model_path MODEL_PATH [--gt_dir GT_DIR]

options:
  -h, --help            show this help message and exit
  --model_path MODEL_PATH
                        The trained model output directory
  --gt_dir GT_DIR       The ground truth dataset directory
```