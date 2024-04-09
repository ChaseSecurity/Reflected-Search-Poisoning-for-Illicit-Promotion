# IPT Contact Extractor

Taking an IPT as the input, our contact extractor is designed to extract all the embedded contact entities.

**The Contact Type Classifier**

This classifier takes an IPT as the input and decides which type of contact it contains. It is built by fine-tuning the `reberta-base` model.

Currently, this classifier supports five contact types which are most frequently embedded in IPTs, and they are `Telephone, Telegram, WeChat, QQ, Website`.

**Contact Entity Extractors**

Given the contact type decided for each IPT, the next step is to extract the respective contact entity. 

For contact types of websites, telephone numbers and QQ accounts, simple rule-based extraction works well thanks to their strict format. 

For the extraction of Telegram and WeChat accounts, we consider them as tasks of named entity recognition (NER). We utilize the aforementioned model to build the two separate NER models for recognizing WeChat and Telegram accounts respectively.