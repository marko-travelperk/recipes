from django.contrib import admin
from .models import Recipe
from .models import Ingredient

# Register your models here.
admin.site.register(Ingredient)

class IngredientInline(admin.TabularInline):
    model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInline
    ]

admin.site.register(Recipe, RecipeAdmin)