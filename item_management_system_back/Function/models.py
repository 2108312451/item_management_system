from django.db import models

# Create your models here.

# 公告
class Notice(models.Model):
    content = models.TextField() #内容
    adminname = models.CharField(max_length=50,default='') #姓名
    times = models.CharField(max_length=50,default='0000-00-00 00:00') #时间
