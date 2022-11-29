import jieba
import csv
import jieba

with open("labeled_contact.csv", mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    all_data = []
    for row in reader:
        all_data.append(row)

index = 0

telegram_data = []
for row in all_data:
    if row[1] == 'telegram':
        seg = jieba.cut(row[0])
        for wd in seg:
            telegram_data.append([index, wd, ''])
        index += 1

qq_data = []
for row in all_data:
    if row[1] == 'qq':
        seg = jieba.cut(row[0])
        for wd in seg:
            qq_data.append([index, wd, ''])
        index += 1


wechat_data = []
for row in all_data:
    if row[1] == 'wechat':
        seg = jieba.cut(row[0])
        for wd in seg:
            wechat_data.append([index, wd, ''])
        index += 1
pass

all_tolabel_data = [['sentence_index', 'word', 'label']]
all_tolabel_data += telegram_data + qq_data + wechat_data

with open('contact_NER_for_labeling.csv', mode='w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerows(all_tolabel_data)