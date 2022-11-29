# Reflected Blackhat SEO

## Crawler

Use a crawler to get reflected blackhat SEO data from search engines. 

Search engines = {Google, Bing, Baidu, Sogou}

## Contact Classify and Named Entity Recognition

Classify which kind of contact methodology an SEO term use. 

contact_methodology = {telegram, website, qq, WeChat, other}

## Terms Binary Classifier

An AdaBoost classifier with 100 estimiters, trained with 2004 positive data (SEO terms) and 1245 negative data (common websites). 

Trying to predict 1,503,817 terms and get 923,665 positive terms and 580,206 negative terms. Sample 3000 positive predicted data and 3000 negative predicted data, then evaluate the performance. 

FN = 32

TN = 2968

FP = 90

TP = 2910

precision = 97%

recall = 98.91%

## Keywords Extract Classifier

A random forest classifier to judge if a segment of an SEO term is a contact information field. 

The contact information keywords are used to crawl more SEO terms in search engines. 

## Terms Multilabel Classifier

Classify a term using a multilabel classifier, to identify the cybercrime activity of the term. 

class = {Drug, Gambling, Surrogacy, Sex & Porn, SEO, Cryptocurrency, General service, Hacker & Crime, Coding & Ghost writing, (Fake) Certificate & Account, Sales & Advertisement, (Fake) Merchandise, SMS, VPN, Financial related, Web Service & App, Benign Terms, Detective, Data service, Unknown}

## Website_Timemachine

A timemachine to crawl websites extracted from SEO terms. 