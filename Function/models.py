from django.db import models

# Create your models here.

# 公告
class Notice(models.Model):
    content = models.TextField() #内容
    adminname = models.CharField(max_length=50,default='') #发布者姓名
    times = models.CharField(max_length=50,default='0000-00-00 00:00') #时间

#借出物品
class Lend(models.Model):
    lenduser_realname = models.CharField(max_length=50,default='') #借用着姓名
    lenditem_id= models.IntegerField(default=0) #借出物品ID
    lenditem_name = models.CharField(max_length=50,default='') #借出物品名称
    lendnumber = models.IntegerField(default=0) #借出数量
    lenditem_grade = models.IntegerField(default=0) #借出物品等级
    lendtime = models.CharField(max_length=50,default='0000-00-00 00:00') #借出时间
    lendday = models.IntegerField(default=0) #借出天数
    approval_progress = models.CharField(max_length=50,default='0%') #进度
    approved_adminname = models.IntegerField(default=-1) #已审批管理员的等级


# 借出审批表
class Approval(models.Model):
    lenduser_realname = models.CharField(max_length=50, default='')  # 借用着姓名
    lenditem_id = models.IntegerField(default=0)  # 借出物品ID
    lenditem_name = models.CharField(max_length=50, default='')  # 借出物品名称
    lendnumber = models.IntegerField(default=0)  # 借出数量
    lenditem_grade = models.IntegerField(default=0)  # 借出物品等级
    lendtime = models.CharField(max_length=50, default='0000-00-00 00:00')  # 借出时间
    lendday = models.IntegerField(default=0)  # 借出天数
    static = models.CharField(max_length=50, default='审核中')  # 状态
    lend = models.ForeignKey(Lend, on_delete=models.CASCADE)  # 关联Lend表的id


# 归还物品
class Returns(models.Model):
    user_realname = models.CharField(max_length=50, default='')  # 归还者姓名
    item_id = models.IntegerField(default=0)  # 归还物品ID
    item_name = models.CharField(max_length=50, default='')  # 归还物品名称
    number = models.IntegerField(default=0)  # 归还数量
    time = models.CharField(max_length=50, default='0000-00-00 00:00')  # 借出时间


# 收藏