import csv



with open("Reflected_Blackhat_SEO_terms_for_labeling - main.csv", mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    all_data = []
    for row in reader:
        all_data.append(row)

labeled_data = []
for item in all_data:
    if item[8] != '':
        if 'wechat' in item[8].lower():
            labeled_data.append([item[0], 'wechat'])
        elif 'website' in item[8].lower():
            labeled_data.append([item[0], 'website'])
        elif 'qq' in item[8].lower():
            labeled_data.append([item[0], 'qq'])
        elif 'telegram' in item[8].lower():
            labeled_data.append([item[0], 'telegram'])
        else:
            labeled_data.append([item[0], 'others'])

with open('labeled_contact.csv', mode='w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerows(labeled_data)

pass