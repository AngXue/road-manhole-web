from django.db import models

from django.db import models


class YolovModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    model_path = models.CharField(max_length=255)
    model_acid = models.FloatField()
    model_parameter = models.IntegerField()
    model_size = models.FloatField()

    def __str__(self):
        return self.name
