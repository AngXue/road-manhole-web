from django.db import models

from django.db import models


class YolovModel(models.Model):
    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=255, unique=True)
    model_path = models.CharField(max_length=255)
    model_acid = models.CharField(max_length=255)
    model_size = models.CharField(max_length=255)
    model_parameter = models.CharField(max_length=255)

    def __str__(self):
        return self.model_name
