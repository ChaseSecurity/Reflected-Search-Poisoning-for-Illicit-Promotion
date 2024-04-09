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
