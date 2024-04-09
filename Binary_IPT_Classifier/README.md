# Binary IPT Classifier

The Random Forest model is chosen as the default binary IPT classifier, as it achieves the best trade-off between prediction performance and inference efficiency.

| **Model**         | **Precision** | **Recall** | **F1 Score** | **Inference Speed** |
|:-----------------:|:-------------:|:----------:|:------------:|:-------------------:|
| **BERT**          | 98.86%        | 98.63%     | 98.75%       | 18(CPU) / 267(GPU)  |
| **Random Forest** | 95.34%        | 97.95%     | 96.63%       | 11667               |
| **Decision Tree** | 95.29%        | 96.81%     | 96.05%       | 13831               |
| **AdaBoost**      | 94.41%        | 96.13%     | 95.26%       | 11510               |
| **SVM**           | 94.39%        | 95.90%     | 95.14%       | 13457               |

Manually Crafted Features:

- **Length in characters.** Most IPTs are lengthy with a median length of 46 characters, but benign texts are more likely to be shorter.

- **Number of bracket-like characters.** IPTs are more likely to have several bracket-like characters (e.g. {, }, [, ], 【, 】) to highlight contact entities.

- **Number of URLs in IPT.** Some IPTs embedding website contact entities may have URLs.

- **Number of numeric characters.** IPTs with WeChat, QQ or telephone contacts often have numeric characters.

- **Number of emojis and unicode symbols.** Some IPTs use emojis or meaningless symbols to make themselves eyecatching.

- **Number of patterns about next-hop instant messaging accounts.** These patterns include `'微信', 'q微', '扣微', '微', '薇', '扣扣', 'qq', 'com', 'fun', 'cc', 'hash', 'tg', 'telegram', '飞机', '@', '网', '复制', 'v信','컴', 'www'`.

- **If there is a file suffix.** Common file suffixes for URLs include `'.html', '.shtml', '.htm', '.php', '.pdf', '.jpg', '.jpeg', '.png', '.xlsx', '.doxx', '.pptx', '.xml'`. Rather than benign URLs, IPTs tend to have no such kinds of suffixes.