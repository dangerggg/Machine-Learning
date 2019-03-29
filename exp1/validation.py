# -*-coding:utf-8-*-
import re
import math

#用于提取特征的正则表达式
feats = [u"[\u4E00-\u9FA5]+", u"(From.*)@(.*)>", u"(X-Mailer): ([a-zA-Z ]+)", u"(X-Priority): ([1-5])"]
root_dir = 'trec06c-utf8/data_cut'
laplace = 1e-50#拉普拉斯平滑参数
alpha = 10#特殊特征的权重


def validation(filepath, feat_set):
    tot = feat_set['spam_cnt'] + feat_set['ham_cnt']
    spam_prop = math.log(feat_set['spam_cnt'] / tot)
    ham_prop = math.log(feat_set['ham_cnt'] / tot)
    with open(filepath) as f:
        src = f.read()
    pattern = re.compile(feats[0])
    result = pattern.findall(src)
    for item in result:
        if item in feat_set['spam'].keys():#计算是垃圾邮件的概率
            spam_prop += math.log(float(feat_set['spam'][item]) / float(feat_set['spam_cnt']))
        else:
            spam_prop += math.log(
                laplace / (feat_set['spam_cnt'] + len(feat_set['spam'].keys()) * laplace))#进行拉普拉斯平滑
            """spam_prop += math.log(
                laplace / feat_set['spam_cnt'])"""#进行常数偏移平滑

        if item in feat_set['ham'].keys():#计算是正常邮件的概率
            ham_prop += math.log(float(feat_set['ham'][item]) / float(feat_set['ham_cnt']))
        else:
            ham_prop += math.log(
                laplace / (feat_set['ham_cnt'] + len(feat_set['ham'].keys()) * laplace))
            """ham_prop += math.log(
                laplace / feat_set['ham_cnt'])"""
    for feat in feats[1:]:
        pattern = re.compile(feat)
        result = pattern.findall(src)
        if len(result) == 0:#对于没有提取到相应特征的邮件的特殊处理
            if feat == "(X-Mailer): ([a-zA-Z ]+)":
                result = [(' ', 'no-Xmailer')]
            elif feat == "(From.*)@(.*)>":
                result = [(' ', 'no-Server')]
            elif feat == u"(X-Priority): ([1-5])":
                result = [(' ', 'no-Priority')]
        else:
            for item in result:
                if item[1] in feat_set['spam'].keys():
                    spam_prop += math.log(
                        float(feat_set['spam'][item[1]]) / float(feat_set['spam_cnt'])) * alpha
                else:
                    spam_prop += math.log(
                        laplace / (feat_set['spam_cnt'] + len(feat_set['spam'].keys()) * laplace)) * alpha
                    """spam_prop += math.log(
                        laplace / feat_set['spam_cnt']) * alpha"""

                if item[1] in feat_set['ham'].keys():
                    ham_prop += math.log(
                        float(feat_set['ham'][item[1]]) / float(feat_set['ham_cnt'])) * alpha
                else:
                    ham_prop += math.log(
                        laplace / (feat_set['ham_cnt'] + len(feat_set['ham'].keys()) * laplace)) * alpha
                    """ham_prop += math.log(
                        laplace / feat_set['ham_cnt']) * alpha"""
    return 'ham' if ham_prop >= spam_prop else 'spam'#取后验概率较大者作为类别返回


def grading(test_set, feat_set):
    test_cnt = 0.0
    bingo = 0.0
    for file in test_set:
        test_cnt += 1
        sp = file.split(" ")
        if sp[0] == validation(root_dir + sp[1][7:], feat_set):
            bingo += 1
    return bingo / test_cnt


