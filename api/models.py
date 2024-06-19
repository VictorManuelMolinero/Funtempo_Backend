from django.db import models
import re

from django.forms import ValidationError

'''
File with all the models that are migrated to the database,
they are serialized with the classes in serializers.py to
transform the data into the database's format
'''

class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)

class Schedule(models.Model):
    starting_hour = models.TimeField()
    finishing_hour = models.TimeField()
    starting_date = models.DateField()
    description = models.CharField(max_length=350)
    username = models.ForeignKey(User, on_delete=models.CASCADE, db_column='username')