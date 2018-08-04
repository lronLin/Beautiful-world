
from hashlib import sha1

from django.db import models
from django.db.models import PROTECT


# 高内聚 低耦合
# 面向对象七个设计原则 : (重点)
    # 1.单一职责原则 2.开闭原则 3.依赖倒转原则 4.里氏替换原则
    #  5.接口隔离原则 6.合成聚合复用原则 7.迪米特法则
# 设计理念 - GoF设计模式
# 创建一个sha1摘要器
# 创建型模式中的原型模式
proto = sha1()


# 定义用户数据模型
class User(models.Model):
    no = models.AutoField(primary_key=True, db_column='uno', verbose_name='编号')
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='口令')
    email = models.CharField(max_length=255, verbose_name='邮箱')
    counter = models.IntegerField(default=3, verbose_name='票数')

    # save方法 - 子类继承父类时对方法进行子类重写父类方法(重点) - 在save时对密码进行摘要
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 外部创建一个对象 - 用时复制对象
        hasher = proto.copy()
        # 更新需要摘要的内容
        hasher.update(self.password.encode('utf-8'))
        # 拿到一个16进制形式的摘要
        self.password = hasher.hexdigest()
        super().save(force_insert, force_update, using, update_fields)

    class Meta(object):
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


# 学科模型
class Subject(models.Model):
    no = models.AutoField(primary_key=True, db_column='sno', verbose_name='编号')
    name = models.CharField(max_length=20, db_column='sname', verbose_name='姓名')
    intro = models.CharField(max_length=1023, db_column='sintro', verbose_name='简介')

    # 对象方法 - 字符串表达式 - 后台管理更直观
    def __str__(self):
        return self.name

    class Meta(object):
        db_table = 'tb_subject'
        # 实体
        verbose_name = '学科'
        verbose_name_plural = '学科'


# Create your models here.
# 自定义模型Teacher一定要继承models - 才能使用ORM框架
# 定义模型
# Django框架中包含了ORM(对象关系映射)框架
# ORM可以帮助我们完成对象模型到关系模型的双向转换
# 数据模型 - 实体模型
class Teacher(models.Model):

    # 拟定老师编号 - 自增长字段AutoField - 设置成主键primary_key - 数据库中对应列db_column
    no = models.AutoField(primary_key=True, db_column='tno', verbose_name='编号')
    # 字符文件CharField - 数据库中对应列db_column
    name = models.CharField(max_length=20, db_column='tname', verbose_name='姓名')
    # job = models.CharField(max_length=10, db_column='tjob', verbose_name='职位')
    intro = models.CharField(max_length=1023, db_column='tintro', verbose_name='简介')
    motto = models.CharField(max_length=255, db_column='tmotto', verbose_name='教学理念')
    # 数据库中存图片存路径 - 不要存二进制数据 - 如果老师没有图片可以设置default=''或者null=True
    photo = models.CharField(max_length=511, db_column='tphoto', verbose_name='照片', null=True, blank=True)
    # 添加外键关联, 空字符时不删除on_delete=PROTECT, 多的一边加ForeignKey , 拒绝做反向查询related_name='+', 加号就是决绝反查(从学科就无法反查老师了)
    subject = models.ForeignKey(Subject, db_column='sno', on_delete=PROTECT, related_name='+', verbose_name='所属学科')
    # 是不是主管
    manager = models.BooleanField(default=False, db_column='tmanager', verbose_name='是否主管')
    # 好评数量 default=0默认值 - 迁移不报错
    good_count = models.IntegerField(default=0, db_column='tgcount', verbose_name='好评数')
    # 差评数量
    bad_count = models.IntegerField(default=0, db_column='tbcount', verbose_name='差评数')

    # 定义属性 - 面向对象 - 属性包装器(重点)
    @property
    def gcount(self):
        return f'{self.good_count}' \
            if self.good_count <= 999 else '999+'

    @property
    def bcount(self):
        return f'{self.bad_count}' \
            if self.bad_count <= 999 else '999+'

    # 在类的里面再定义一个类 - 称之为类部类 - 必须写成Meta
    class Meta(object):
        # Teacher类对应数据库里的表
        db_table = 'tb_teacher'
        verbose_name = '讲师'
        verbose_name_plural = '讲师'
        # 加-号降序排列 / 没有加就是升序排列
        ordering = ('name', )






