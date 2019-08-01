from django.db import models
from enum import Enum


class Product(models.Model):
    name = models.CharField(max_length=20)
    calories = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}:{self.name}  -  {str(self.calories)} cal/100g"


class User(models.Model):
    user_name = models.CharField(max_length=20)
    weight = models.IntegerField()
    height = models.IntegerField()
    age = models.DateField()
    sex = models.BooleanField()


class MealChoice(Enum):
    Breakfast = 1
    Lunch = 2
    Dinner = 3
    Snacks = 4


class Meal(models.Model):
    meal_type = models.IntegerField(default=0)
    day = models.DateField(auto_now=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        chosen_products = ", ".join(str(product) for product in self.products.all())
        return "{},{}".format(self.day, chosen_products)
