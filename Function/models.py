from django.db import models

# Create your models here.

# 公告
class Notice(models.Model):
    content = models.TextField() #内容
    adminname = models.CharField(max_length=50,default='') #发布者姓名
    times = models.CharField(max_length=50,default='0000-00-00 00:00') #时间

#借用物品
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
    lenduser_realname = models.CharField(max_length=50, default='')  # 借用者姓名
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
    time = models.CharField(max_length=50, default='0000-00-00 00:00')  # 归还时间


# 收藏
class Collections(models.Model):
    item_id = models.IntegerField(default=0)  # 物品ID
    item_name = models.CharField(max_length=50, default='')  #物品名称
    username = models.CharField(max_length=50, default='')  # 用户姓名

# 报修（设备）
class Repairs(models.Model):
    item_id = models.IntegerField(default=0)  # 设备ID
    item_name = models.CharField(max_length=50, default='')  # 设备名称
    adress = models.CharField(max_length=50, default='')  # 设备地址
    username = models.CharField(max_length=50, default='')  # 申报人姓名
    text = models.TextField(default='') # 维修问题
    times = models.CharField(max_length=50, default='0000-00-00 00:00')  #时间
    statics = models.BooleanField(default=False) #维修状态(未维修/已经处理)

# 反馈
class Feedback(models.Model):
    item_id = models.IntegerField(default=0)  # 物品ID
    item_name = models.CharField(max_length=50, default='')  # 物品名称
    adress = models.CharField(max_length=50, default='')  # 物品地址
    username = models.CharField(max_length=50, default='')  # 反馈人姓名
    text = models.TextField(default='')  # 反馈问题
    times = models.CharField(max_length=50, default='0000-00-00 00:00')  # 时间
    statics = models.BooleanField(default=False)  # 状态(未处理/已经处理)

# 对话内容
class HelpCenterContent(models.Model):
    text = models.TextField(default='') #内容
    identity = models.CharField(max_length=10,default='') #该消息所属对象（管理员/用户）
    times = models.CharField(max_length=50, default='0000-00-00 00:00')  #发送消息时间
    HelpCenterid = models.IntegerField(default=0) #那次对话id

# 记录每段对话
class HelpCenterSave(models.Model):
     #主键id为每段对话id
    firsttext = models.TextField(default='') #第一句话
    userid = models.IntegerField(default=0) #用户id
    username = models.CharField(max_length=50, default='') #用户姓名
    handleadminid = models.IntegerField(default=0) #处理改对话管理员id
    handleadmin = models.CharField(max_length=50, default='') #处理改对话管理员姓名
    times = models.CharField(max_length=50, default='0000-00-00 00:00')  #对话生成时间
    statics = models.BooleanField(default=False)  # 对话是否完成

