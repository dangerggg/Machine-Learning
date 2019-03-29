# -*-coding:utf-8-*-
import re

# regrex to filter information from mails
feats = [u"[\u4E00-\u9FA5]+", u"(From.*)@(.*)>", u"(X-Mailer): ([a-zA-Z ]+)", u"(X-Priority): ([1-5])"]
root_dir = 'trec06c-utf8/data_cut'


def training_spilter(feat_set, filename):
    file = filename.split(" ")
    if file[0] == 'spam':
        feat_set['spam_cnt'] += 1
    elif file[0] == 'ham':
        feat_set['ham_cnt'] += 1
    with open(root_dir + file[1][7:]) as f:
        src = f.read()
    for feat in feats:
        pattern = re.compile(feat)
        result = pattern.findall(src)
        if len(result) == 0:#对于没有提取到相应特征的邮件的特殊处理
            if feat == u"(X-Mailer): ([a-zA-Z ]+)":
                result = [(' ', 'no-Xmailer')]
            elif feat == u"(From.*)@(.*)>":
                result = [(' ', 'no-Server')]
            elif feat == u"(X-Priority): ([1-5])":
                result = [(' ', 'no-Priority')]
        for item in result:
            if isinstance(item, str):
                if item in feat_set[file[0]].keys():
                    feat_set[file[0]][item] += 1
                else:
                    feat_set[file[0]][item] = 1
            else:
                if item[1] in feat_set[file[0]].keys():
                    feat_set[file[0]][item[1]] += 1
                else:
                    feat_set[file[0]][item[1]] = 1
    #print("finish " + file[1])
    return feat_set






