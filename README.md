# Reflected Blackhat SEO

## Crawler

Use a crawler to get reflected blackhat SEO data from search engines. 

Search engines = {Google, Bing, Baidu, Sogou}

## Contact Classify and Named Entity Recognition

Classify which kind of contact methodology an SEO term use. 

contact_methodology = {telegram, website, qq, WeChat, other}

## Terms Binary Classifier

An AdaBoost classifier with 100 estimiters, trained with 2004 positive data (SEO terms) and 1245 negative data (common websites). 

## Keywords Extract Classifier

A random forest classifier to judge if a segment of an SEO term is a contact information field. 

The contact information keywords are used to crawl more SEO terms in search engines. 

## Terms Multilabel Classifier

Classify a term using a multilabel classifier, to identify the cybercrime activity of the term. 

class = {Drug, Gambling, Surrogacy, Sex & Porn, SEO, Cryptocurrency, General service, Hacker & Crime, Coding & Ghost writing, (Fake) Certificate & Account, Sales & Advertisement, (Fake) Merchandise, SMS, VPN, Financial related, Web Service & App, Benign Terms, Detective, Data service, Unknown}

## Contact Information Extraction

Use some methods to extract contact information embedding in terms. 

Now finished extracting websites, and telegram accounts. 

## Website Timemachine

A time machine to crawl websites extracted from SEO terms. 

## Telegram Timemachine

A time machine to crawl telegram accounts extracted from SEO terms.

## Website Screenshot Classifier

Classify a website using a multimodal classifier based on the screenshot of its landing page output by `time_machine.py` and the text content extracted from it by OCR, to identify the cybercrime activity of the website.

class = {(Fake) Certificate & Account & Merchandise, Drug, Financial related, Gambling, Benign, Hacker & Crime, Sales & Advertisement, SEO, Sex & Porn, Unknown, Redirection Page, Domain Expired}