path = 'result/result_from_contact.txt'

with open(path, 'r', encoding='utf-8') as fp:
    all_data = fp.readlines()

data_turples = []
positive_data_predicted = []
negative_data_predicted = []
for item in all_data:
    try:
        turp = eval(item)
        term = turp[0]
        data_turples.append(turp)
    except:
        if (item == '\n'):
            pass
        else:
            lst = item.split(')(\'')
            data_turples.append(eval(lst[0] + ')'))
            data_turples.append(eval('(\'' + lst[1]))
        print('Fix Error on line' + str(len(data_turples)))

with open(path, 'w', encoding='utf-8') as fp:
    for item in data_turples:
        fp.write(str(item))
        fp.write('\n')




path = 'result/result_from_site.txt'

with open(path, 'r', encoding='utf-8') as fp:
    all_data = fp.readlines()

data_turples = []
positive_data_predicted = []
negative_data_predicted = []
for item in all_data:
    try:
        turp = eval(item)
        term = turp[0]
        data_turples.append(turp)
    except:
        if (item == '\n'):
            pass
        else:
            lst = item.split(')(\'')
            data_turples.append(eval(lst[0] + ')'))
            data_turples.append(eval('(\'' + lst[1]))
        print('Fix Error on line' + str(len(data_turples)))

with open(path, 'w', encoding='utf-8') as fp:
    for item in data_turples:
        fp.write(str(item))
        fp.write('\n')