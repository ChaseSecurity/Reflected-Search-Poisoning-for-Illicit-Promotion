import re

def non_alphanumeric_num(term):
    cnt = 0
    for s in term:
        if (not s.isalpha()) and (not s.isdecimal()):
            cnt += 1
    return cnt

def alphanumeric_num(term):
    cnt = 0
    for s in term:
        if s.isalpha() or s.isdecimal():
            cnt += 1
    return cnt

def numeric_num(term):
    cnt = 0
    for s in term:
        if s.isdecimal():
            cnt += 1
    return cnt

def patterns_num(term):
    patterns = ['微信', 'q微', '扣微', '微', '薇', '扣扣', 'qq',\
                'com', 'fun', 'cc', 'hash', 'tg', 'telegram', \
                '飞机', '@', '网', '复制']
    cnt = 0
    for p in patterns:
        if p in term.lower():
            cnt += 1
    return cnt

def punctuation_num(term):
    patterns =  ['.', ':', '：', '·', 'ͺ', '-']
    cnt = 0
    for p in patterns:
        if p in term.lower():
            cnt += 1
    return cnt

def brackets_num(term):
    brackets_num = ['[', ']', '【', '】', '(', ')', '（',\
                '）', '『', '』', '《', '》', '<', \
                '>', '☀️', '👉']
    cnt = 0
    for p in brackets_num:
        if p in term:
            cnt += 1
    return cnt

def has_suffix(term):
    suffix = ['.html', '.shtml', '.htm', '.php', '.pdf', '.jpg', '.jpeg', '.png', '.xlsx', '.doxx', '.pptx', '.xml']
    for s in suffix:
        if s in term:
            return 1
    return 0

def url_num(term):
    url_pattern = r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?'
    return len(re.findall(url_pattern, term))