import csv



with open("Reflected_Blackhat_SEO_terms_for_labeling - main.csv", mode="r", encoding="utf-8") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    all_data = []
    for row in reader:
        all_data.append(row)

labeled_data = []
for item in all_data:
    if item[1] != '':
        labeled_data.append(item[:5])

with open('labeled_terms.csv', mode='w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerows(labeled_data)

pass