# IPT Keyword Extractor

The contact segment of an IPT turns out to be good search keywords in terms of guiding the search engines and discovering new RSPs/IPTs.

A Random Forest Classifier is applied to decide whether a given IPT segment is a contact segment or not.

The list of features:

- **Length in characters.** The contact segments are more likely to be shorter than other segments of IPTs.

- **Number of URLs in IPT.** Some segments of IPTs embedding website contact entities may have URLs.

- **Number of non-alphanumeric characters.** The contact segments are more likely to have fewer non-alphanumeric characters than other segments of IPTs.

- **Number of alphanumeric characters.** The contact segments are more likely to have more alphanumeric characters than other segments of IPTs.

- **Number of numeric characters.** Segments with WeChat, QQ or telephone contacts often have numeric characters.

- **Number of contact indicators.** The indicators of next-hop contacts include `'微信', 'q微', '扣微', '微', '薇', '扣扣', 'qq', 'com', 'fun', 'cc', 'hash', 'tg', 'telegram', '飞机', '@', '网', '复制'`.

- **Number of some common punctuation marks in terms.** Various punctuation symbols are used to separate an IM mark and the respective IM account identifier. Symbols under our consideration include `'.', ':', '：', '·', 'ͺ', '-'`.

- **If there is a file suffix.** Common file suffixes for URLs include `'.html', '.shtml', '.htm', '.php', '.pdf', '.jpg', '.jpeg', '.png', '.xlsx', '.doxx', '.pptx', '.xml'`. Rather than benign URLs, IPTs tend to have no such kinds of suffixes.

The output model can be found [here](../Search_Engine_Crawler/model/random_forest_model_keywords.pickle)