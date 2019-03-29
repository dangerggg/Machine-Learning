> 姓名：曾军
>
> 学号：2016011359
>
> 手机：13121011966

> 文件组织：
>
> shell.py：程序的总入口
>
> model_training.py：模型训练模块
>
> validation.py：验证测试模块
>
> plot.py：绘图模块

> 运行：
>
> 运行shell.py，输入train可以根据自己选择的训练集/测试集的比例进行训练，训练好的模型存在feat_set.pkl中，且测试集存在test_set.pkl中
>
> 输入validation可以判断某个给定路径的电子邮件是否是垃圾邮件，此时需要加载自己的模型
>
> 输入grading可以使用测试集对训练出来的模型进行正确率评价
>
> 输入cross-examination可以进行五折交叉验证，没有将结果存在内存中，经过多次测试应该可以复现
>
> 运行plot.py可以绘制相应的图案