from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    owner = models.CharField(max_length=20)
    modelid = models.DecimalField(max_digits=5, decimal_places=2)
    accur = models.DecimalField(max_digits=5, decimal_places=2)
    visible = models.IntegerField()