import validation as val
import model_training as modeling
import _pickle as cPickle
import random
import numpy as np

dataset_path = 'trec06c-utf8/data_cut/'
label_path = 'trec06c-utf8/label/index'
label = []
train_set = []
test_set = []
random_averaging_set = []
feat_set = {
    'spam': {'total': 0},
    'ham': {'total': 0},
    'spam_cnt': 0,
    'ham_cnt': 0
}
folders = 5
recept_prop = 1#使用多少比例的训练集
#random.seed(1)


def dump2disk(option):#将训练结果存到磁盘中
    global feat_set
    global test_set
    global random_averaging_set
    if option == 'w':
        with open('feat_set.pkl', 'wb') as f:
            cPickle.dump(feat_set, f)
        with open('test_set.pkl', 'wb') as h:
            cPickle.dump(test_set, h)
        with open('random_averaging_set.pkl', 'wb') as g:
            cPickle.dump(random_averaging_set, g)
    elif option == 'r':
        with open('feat_set.pkl', 'rb') as f:
            feat_set = cPickle.load(f)
        with open('test_set.pkl', 'rb') as h:
            test_set = cPickle.load(h)
        with open('random_averaging_set.pkl', 'rb') as g:
            random_averaging_set = cPickle.load(g)


def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def boot_loader(label_path, percentage):#从数据集中按一定比例分出训练集和测试集并进行训练
    global label
    label = read_file(label_path).split('\n')[:-1]
    for item in label:
        if random.uniform(0, 1) < percentage:
            train_set.append(item)
        else:
            test_set.append(item)
    for filename in train_set:
        if random.uniform(0, 1) < recept_prop:
            training(filename)
    dump2disk('w')# 将训练结果写入磁盘


def training(filename):#调用训练模块
    global feat_set
    feat_set = modeling.training_spilter(feat_set, filename)


def validation(option, filename):#调用验证模块
    if option == 'validation':
        return val.validation(filename, feat_set)
    elif option == 'grading':
        return val.grading(test_set, feat_set)


def cross_examination():#调用训练和验证模块进行五折交叉验证，使用shuffle()操作打乱列表排序
    global label
    global random_averaging_set
    result = []
    label = read_file(label_path).split('\n')[:-1]
    random.shuffle(label)
    for i in range(0, folders):
        random_averaging_set.append(label[int(len(label) * i / 5):int(len(label) * (i + 1) / 5)])

    for i in range(0, folders):
        cross_set = {
            'spam': {'total': 0},
            'ham': {'total': 0},
            'spam_cnt': 0,
            'ham_cnt': 0
        }
        for j in range(0, folders):
            if i != j:
                for filename in random_averaging_set[j]:
                    if random.uniform(0, 1) < recept_prop:
                        cross_set = modeling.training_spilter(cross_set, filename)
        result.append(val.grading(random_averaging_set[i], cross_set))
    print(result)
    print("min: " + str(np.min(result)))
    print("max: " + str(np.max(result)))
    print("average: " + str(np.average(result)))
    print()


def main():
    global recept_prop
    op = input("train, grading, filtering or cross-examination\n")
    if op == 'filtering':
        dump2disk('r')
        op = input("the filepath:\n")
        print(validation('validation', op))
    elif op == 'grading':
        dump2disk('r')
        print(validation('grading', ' '))
    elif op == 'train':
        op = input("choose how much percentage of the dataset you want to use to train:\n")
        op = float(op)
        boot_loader(label_path, op)
    elif op == 'cross-examination':
        cross_examination()


if __name__ == "__main__":
    main()


