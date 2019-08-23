from django.test import TestCase
from django.urls import reverse
from recipesapp.models import Recipe, Ingredient


# Create your tests here.

class RecipeTest(TestCase):
    def test_get_recipes(self):
        recname = 'recipe1'
        recprocedure = 'make'
        rec = Recipe.objects.create(name= recname, procedure=recprocedure)
        expected_recipe = {'name':recname, 'procedure':recprocedure, 'id':1,'ingredients': []}
        response = self.client.get('/recipes/')
        self.assertTrue(response.status_code == 200)
        self.assertDictEqual(response.json().get('results')[0], expected_recipe)

        ingredient = Ingredient.objects.create(name="ingredient", recipe=rec)
        expected_recipe.update('ingredients', [{'id':'1', 'name':'ingredient'}])
        response = self.client.get('/recipes/')
        self.assertTrue(response.status_code == 200)
        self.assertDictEqual(response.json().get('results')[0], expected_recipe)

        putresponse = self.client.put('/recipes/1/')