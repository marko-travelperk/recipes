from collections import OrderedDict

from recipesapp.models import Recipe, Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(allow_empty=True, many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'procedure', 'ingredients']

    def create(self, validated_data):
        ingredients_data = []
        if 'ingredients' in validated_data.keys():
            ingredients_data = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = []

        if 'ingredients' in validated_data.keys():
            ingredients_data = validated_data.pop('ingredients')

        if 'name' in validated_data.keys():
            instance.name = validated_data.pop('name')

        if 'procedure' in validated_data.keys():
            instance.procedure = validated_data.pop('procedure')

        oldingredients_data = instance.ingredients.values()
        if oldingredients_data:
            for oldingredient in oldingredients_data:
                Ingredient.objects.get(id = oldingredient.get("id")).delete()

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(name=ingredient_data.get("name"), recipe=instance)

        instance.save()
        return instance
