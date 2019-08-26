from django.db import models
from django.utils import timezone

# Create your models here.
class Recipe(models.Model):
    name = models.TextField()
    procedure = models.TextField()

class Ingredient(models.Model):
    name = models.TextField()
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
