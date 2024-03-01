from django.db import models

# Create your models here.
#----加密
# from django.contrib.auth.hashers import make_password
#
# # 原始密码字符串
# password = "123456"
#
# # 使用 make_password 函数加密密码
# hashed_password = make_password(password)
#----验证
# from django.contrib.auth.hashers import check_password
#
# # 存储在数据库中的加密密码
# hashed_password = "..."
#
# # 用户输入的原始密码
# password = "123456"
#
# # 使用 check_password 函数验证密码是否匹配
# is_matched = check_password(password, hashed_password)

# 普通用户
class OrdinaryUser(models.Model):
    realname = models.CharField(max_length=100,default='') #真实姓名
    username = models.CharField(max_length=100,default='') #用户名
    password = models.CharField(max_length=300,default='') #哈希密码
    phone = models.CharField(max_length=100,default='') #电话
    reputation = models.IntegerField(default=100) #信誉分
    group = models.CharField(max_length=10,default='') #组别
    status = models.BooleanField(default=True) #状态
    privilege_level = models.IntegerField(default=0) #权限等级 0

# 验证码
class Codes(models.Model):
    Code = models.CharField(max_length=10,default='')

# 管理员
class Regular_Administrator(models.Model):
    realname = models.CharField(max_length=100, default='')  # 真实姓名
    username = models.CharField(max_length=100, default='')  # 用户名
    password = models.CharField(max_length=300, default='')  # 哈希密码
    phone = models.CharField(max_length=100, default='')  # 电话
    status = models.BooleanField(default=True) #状态
    privilege_level = models.IntegerField(default=1)  # 权限等级 1

# 超级管理员
class Super_Administrator(models.Model):
    realname = models.CharField(max_length=100, default='')  # 真实姓名
    username = models.CharField(max_length=100, default='')  # 用户名
    password = models.CharField(max_length=300, default='')  # 哈希密码
    phone = models.CharField(max_length=100, default='')  # 电话
    status = models.BooleanField(default=True)  # 状态
    privilege_level = models.IntegerField(default=2)  # 权限等级 2






