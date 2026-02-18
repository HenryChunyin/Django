from django.db import models
import datetime
from django.utils.timezone import now

class Person(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)


class Model(models.Model):
    name = models.CharField(max_length=50)


class Department(models.Model):
    ''' 部门表 '''
    # 默认有id列，主键自增。
    name = models.CharField(max_length=32, verbose_name='标题')

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    ''' 员工表 '''
    # 性别选项
    gender_choices = (
        (1, "男"),
        (2, "女")
    )

    name = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    amount = models.DecimalField(
        max_digits=10,  # 有效数字位数10
        verbose_name='账户余额',
        decimal_places=2,  # 小数位数2
        default=0,
    )

    create_time = models.DateTimeField(verbose_name='入职时间')

    depart = models.ForeignKey(
        to='Department',
        to_field='id',  # 字段名小写

        # 当关联的表中数据删除时，本字段值有两种处理方式：
        # 1. 级联删除（也跟着删除）
        # on_delete=models.CASCADE, #级联删除
        # 2. 置空
        on_delete=models.SET_NULL,  # 置空
        null=True, blank=True,  # 置空的前提是该字段允许为空
        verbose_name='部门名称'
    )

    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, null=True, blank=True)

    def __str__(self):
        return self.name


class ExperimentProject(models.Model):
    '''实验项目'''
    proj_num = models.CharField(max_length=20, verbose_name='Proj Code')
    proj_name = models.CharField(max_length=50, verbose_name='Name')

    status_choices = (
        (1, 'Marketing Investigation'),
        (2, 'Reviewing'),
        (3, 'Developing'),
        (4, 'Small-scale trial'),
        (5, 'Middle-scale trial'),
        (6, 'Manufacture')
    )
    proj_stat = models.SmallIntegerField(verbose_name='Status', choices=status_choices, default=1, null=True,
                                         blank=True)

    apply_time = models.DateField(verbose_name='Starting Date', default=now())
    proof_time = models.DateField(verbose_name='Development', null=True, blank=True)
    rd_time = models.DateField(verbose_name='Primary Complete', null=True, blank=True)
    try_produ_time = models.DateField(verbose_name='Mid-scale Trial', null=True, blank=True)
    production_time = models.DateField(verbose_name='Manufacture Trial', null=True, blank=True)


class ExperimentRecord(models.Model):
    '''实验记录表'''
    record_num = models.CharField(max_length=20, verbose_name='单号')
    proj_name = models.ForeignKey(verbose_name='所属项目', to='ExperimentProject', to_field='id',
                                  on_delete=models.CASCADE)
    record_time = models.DateField(verbose_name='实验日期')
    expr_name = models.CharField(max_length=50, verbose_name='实验名称')
    target = models.CharField(max_length=200, verbose_name='实验目的')
    program = models.CharField(max_length=800, verbose_name='实验方案')
    results = models.CharField(max_length=800, verbose_name='实验结果与分析')
    conclusion = models.CharField(max_length=50, verbose_name='实验结论')


class Oder(models.Model):
    '''订单'''
    oder_num = models.CharField(max_length=20, verbose_name='订单号')
    proj_name = models.CharField(max_length=32, verbose_name='名称')
    price = models.IntegerField(verbose_name='价格')
    status_choises=(
        (1, '待支付'),
        (2, '已支付')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choises, default=1)
    user_id = models.ForeignKey(to=UserInfo, verbose_name='用户ID', on_delete=models.CASCADE)
