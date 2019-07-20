from django.db import models


'''
Create your models here.
create cmd : 通过模型类在数据库中创建表
python manage.py makemigrations  
python manage.py migrate  
'''
#定义模型--数据库中的表
class Player(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    position = models.CharField(max_length=10)
    number = models.IntegerField()