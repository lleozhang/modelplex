from django.db import models


class ModInfo(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 1000)
    accuracy=models.FloatField()
    owner = models.CharField(max_length = 10)
    add = models.CharField(max_length=1000)
    tests = models.IntegerField()
    homepage = models.CharField(max_length=1000)

