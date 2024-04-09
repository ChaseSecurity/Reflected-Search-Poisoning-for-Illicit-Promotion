# Reflected Search Poisoning for Illicit Promotion

[![Paper](http://img.shields.io/badge/Paper-arXiv.2404.05320-B3181B?logo=arXiv)](https://arxiv.org/abs/2404.05320)

## Search Engine Crawler

Deploy a crawler to obtain reflected search poisoning data from four search engines: Google, Bing, Baidu, Sogou.

## Binary IPT Classifier

A Random Forest classifier trained with 2,229 positive data and 1,468 negative data to distinguish RSPs from benign URL reflections. 

## IPT Keyword Extractor

A Random Forest classifier trained with 1,012 positive data and 3,170 negative data to decide whether an IPT segment is a contact segment or not, which is a good search keyword in terms of guiding the search engines and discovering new RSPs/IPTs.

## Multi-label IPT Classifier

By fine tuning the multilingual BERT model, we build this classifier to classify IPT as either a harmless 'Benign' category or one or more of the 14 illicit services/goods categories.

## IPT Contact Extractor

Taking an IPT as the input, our contact extractor is designed to extract all the embedded contact entities, which is achieved by a contact type classifier and contact entity extractors.

## Website Dynamic Crawler

By instrumenting a headless browser, we capture the final landing webpage as a screenshot and save all the network traffic of both HTTP requests and HTTP responses. 

## Telegram Account Infiltrator

Leveraging publicly available Telegram APIs, we can extract the profile of each Telegram account at a weekly pace.
