from django.db import models

# Create your models here.
class Items(models.Model):
    item_name = models.CharField(max_length=100,default='') #名称
    item_code = models.CharField(max_length=100,default='') #编号
    value = models.DecimalField(max_digits=10, decimal_places=2) #价值(整数/浮点)
    specifications = models.TextField() #规格
    category = models.CharField(max_length=100,default='') #类别
    brand = models.CharField(max_length=100,default='') #品牌
    inventory = models.IntegerField() #库存
    campus = models.IntegerField() #校区 1&2
    location = models.CharField(max_length=100,default='') #存放地址
    max_quantity = models.IntegerField() #最大申请数量
    instructions = models.TextField() #操作说明
    pictureUrl = models.CharField(max_length=100,default='') #图片地址
    approval_classification = models.IntegerField() #物品等级 1/2/3
    frequency_use = models.IntegerField(default=0) #使用频率

# 评论
class Comments(models.Model):
    comment_text = models.TextField(default='')
    comment_username = models.CharField(max_length=50,default='')
    comment_itemid = models.IntegerField()
    comment_times = models.CharField(max_length=50,default='0000-00-00 00:00')

# 入库（添加物品）
class Warehousing(models.Model):
    item_name = models.CharField(max_length=100, default='')  # 名称
    item_code = models.CharField(max_length=100, default='')  # 编号
    category = models.CharField(max_length=100, default='')  # 类别
    brand = models.CharField(max_length=100, default='')  # 品牌
    numbers = models.IntegerField()  # 入库数量
    location = models.CharField(max_length=100, default='')  # 存放地址
    approval_classification = models.IntegerField(default=0)  # 物品等级
    times = models.CharField(max_length=50,default='0000-00-00 00:00') #入库时间

# 出库（删除，维修报废物品）
class Outbound(models.Model):
    item_name = models.CharField(max_length=100, default='')  # 名称
    item_code = models.CharField(max_length=100, default='')  # 编号
    category = models.CharField(max_length=100, default='')  # 类别
    brand = models.CharField(max_length=100, default='')  # 品牌
    numbers = models.IntegerField()  # 出库数量
    approval_classification = models.IntegerField()  # 物品等级
    Reason_Outbound = models.IntegerField(default=0) #出库原因，正常删除还是报废(1删除/0报废)
    times = models.CharField(max_length=50, default='0000-00-00 00:00') #出库时间