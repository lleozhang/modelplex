from django.db import models

class History(models.Model):
    hacker = models.CharField(max_length=20)
    model_id = models.IntegerField()
    dataset_id = models.IntegerField()
    dataset_number = models.IntegerField()
    accuracy = models.FloatField()
    recall = models.FloatField()
    loss = models.FloatField()
