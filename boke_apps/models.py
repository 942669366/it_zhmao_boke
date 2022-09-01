from django.db import models

# Create your models here.

class poetry(models.Model):
    # __tablename__ = "poetry"
    poetrys_id = models.IntegerField(primary_key = True)
    # # unique表示会否允许重复出现，nullable表示会否允许为空
    poetrys = models.CharField(max_length = 1000)

class poetry2(models.Model):
    # __tablename__ = "poetry"
    poetrys_id = models.IntegerField(primary_key=True)
    # # unique表示会否允许重复出现，nullable表示会否允许为空
    poetrys = models.CharField(max_length=1000)

class user_data(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=10)
    user_pwd = models.CharField(max_length=15)


