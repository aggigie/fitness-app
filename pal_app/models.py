from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=20)
    calories = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}  -  {str(self.calories)} cal/100g"


class User(models.Model):
    user_name = models.CharField(max_length=20)
    weight = models.IntegerField()
    height = models.IntegerField()
    age = models.IntegerField()
    sex = models.BooleanField()
