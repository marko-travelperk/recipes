from collections import OrderedDict

from recipesapp.models import Recipe, Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(allow_empty=True, many=True, required=False)  # , read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'procedure', 'ingredients']

    def create(self, validated_data):
        ingredients_data = []
        if validated_data.__contains__('ingredients'):
            ingredients_data = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = []

        if validated_data.__contains__('ingredients'):
            ingredients_data = validated_data.pop('ingredients')

        oldingredients_data = []
        if hasattr(instance, 'ingredients'):
            oldingredients_data = instance.ingredients

        oldlist = list(map(lambda x: x.get("name"), oldingredients_data.values()))

        newlist = list(map(lambda x: x.get("name"), ingredients_data))

        removediff = set(oldlist)-set(newlist)
        print(removediff)

        adddiff = set(newlist) - set(oldlist)
        print(adddiff)

        print(instance.id)

        if validated_data.__contains__('name'):
            instance.name = validated_data.pop('name')

        if validated_data.__contains__('procedure'):
            instance.procedure = validated_data.pop('procedure')

        for ingredient_data in adddiff:
            Ingredient.objects.update_or_create(name=ingredient_data, recipe=instance)

        for ingredient_data in removediff:
            if not self.partial:
                Ingredient.objects.get(name=ingredient_data, recipe=instance).delete()

        instance.save()
        return instance
