from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from recipesapp.models import Recipe, Ingredient
from recipesapp.serializers import RecipeSerializer
from recipesapp.views import RecipeViewSet
from rest_framework.test import RequestsClient
from requests import request
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'recipes.settings'
import django
django.setup()
# Create your tests here.

class ModelsTest(TestCase):
    def test_create(self):
        recName = "recipename"
        procedure="recipeprocedure"
        ingredientName = "ingredient"
        Recipe.objects.create(name=recName, procedure=procedure)
        recipes = Recipe.objects.all()
        self.assertEqual(len(Recipe.objects.all()),1)
        self.assertEqual(recipes[0].name, recName)
        self.assertEqual(recipes[0].procedure, procedure)

        # Create and add an ingredient
        Ingredient.objects.create(name=ingredientName, recipe=recipes[0])

        all_ingredients = Ingredient.objects.all()
        self.assertEqual(len(all_ingredients), 1)

        # Delete the recipe, verify both recipe and ingredient were deleted
        Recipe.objects.get(id=1).delete()

        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 0)

        all_ingredients = Ingredient.objects.all()
        self.assertEqual(len(all_ingredients), 0)

class ViewsTest(TestCase):
    def test_getemptyset(self):
        viewset = RecipeViewSet()
        result = viewset.get_queryset()
        self.assertEqual(len(result), 0)

    def test_fetchrecipes(self):
        Recipe.objects.create(name= "na123me", procedure="proc789edure")
        Recipe.objects.create(name= "na456me", procedure="proce899dure")

        # Fetch all recipes
        request = APIRequestFactory().get("recipes");
        viewset = RecipeViewSet.as_view({'get':'list'})
        result = viewset(request)

        self.assertEqual(len(result.data), 2)
        self.assertContains(result, 'na123me')
        self.assertContains(result, 'na123me')

        # Get both recipes with name start
        request = APIRequestFactory().get("recipes?name=na1")
        viewset = RecipeViewSet.as_view({'get':'list'})
        result = viewset(request)

        self.assertEqual(len(result.data), 1)
        self.assertContains(result, 'na123me')

        #Verify empty string doesn't break querying
        request = APIRequestFactory().get("recipes?name=")
        viewset = RecipeViewSet.as_view({'get':'list'})
        result = viewset(request)

        self.assertEqual(len(result.data), 2)
        self.assertContains(result, 'na123me')
        self.assertContains(result, 'na456me')

        # Fetch both recipes with general query
        request = APIRequestFactory().get("recipes?q=89")
        viewset = RecipeViewSet.as_view({'get':'list'})
        result = viewset(request)

        self.assertEqual(len(result.data), 2)
        self.assertContains(result, 'na123me')
        self.assertContains(result, 'na456me')

        # Verify empty query
        request = APIRequestFactory().get("recipes?q=")
        viewset = RecipeViewSet.as_view({'get':'list'})
        result = viewset(request)

        self.assertEqual(len(result.data), 2)
        self.assertContains(result, 'na123me')
        self.assertContains(result, 'na456me')

        # Return empty list
        request = APIRequestFactory().get("recipes?q=777")
        viewset = RecipeViewSet.as_view({'get':'list'})
        result = viewset(request)

        self.assertEqual(len(result.data), 0)

class SerializerTest(TestCase):
    recipejson=""
    recipeobj = {}

    def setUp(self):
        self.recipejson={
            "name": "validName",
            "procedure" : "validProcedure",
            "ingredients" : [
                {
                "name" : "validing1"
                },
                {
                "name": "validing2"
                }
            ]
        }

        self.recipeobj = RecipeSerializer().create(validated_data=self.recipejson)

    def test_createrecipe(self):
        self.assertEqual("validName", self.recipeobj.name)
        self.assertEqual("validProcedure", self.recipeobj.procedure)

    def test_putrecipe(self):
        updaterecipejson = {
            "name": "replacename",
            "procedure": "replaceProcedure",
            "ingredients": [
                { "name" : "ingr3"}
            ]
        }

        recipeobj = RecipeSerializer().update(self.recipeobj, validated_data=updaterecipejson)

        self.assertEqual("replacename", recipeobj.name)
        self.assertEqual("replaceProcedure", recipeobj.procedure)

    def test_patchrecipe(self):

        updaterecipejson = {
            "name": "replaceonlyname"
        }

        recipeobj = RecipeSerializer().update(self.recipeobj, validated_data=updaterecipejson)

        self.assertEqual("replaceonlyname", recipeobj.name)
        self.assertEqual("validProcedure", recipeobj.procedure)

class RestApiTest(TestCase):
    factory = APIRequestFactory()

    def setUp(self) :
        self.getviewset = RecipeViewSet.as_view({'get': 'list'})
        self.get_request = self.factory.get("/recipes");
        self.r = Recipe.objects.create(name="name1", procedure="procedure1")
        Ingredient.objects.create(name="ingred1", recipe=self.r)
        Ingredient.objects.create(name="ingred2", recipe=self.r)

    def test_POST(self):
        post_request = self.factory.post("/recipes/", json.dumps(
            {"name": "name2", "procedure": "procedure2", "ingredients": [{"name": "ingred3"}, {"name": "ingred4"}]}),
                                    content_type='application/json')

        viewset = RecipeViewSet.as_view({'post': 'create'})

        result = viewset(post_request)
        self.assertContains(result, "name2", status_code=201)
        new_id = result.data['id']
        self.assertEqual(2, len(Recipe.objects.all()));

        result = self.getviewset(self.get_request)
        self.assertContains(result, "name2", status_code=200)

        newRecipe = [x for x in list(result.data) if x['id'] == new_id][0]
        self.assertEqual(newRecipe['name'], "name2")
        self.assertEqual(newRecipe['procedure'], "procedure2")
        self.assertEqual([x['name'] for x in newRecipe['ingredients']], ["ingred3", "ingred4"])

        self.assertEqual(Recipe.objects.get(id=new_id).name, 'name2')

    def test_GET(self):
        result = self.getviewset(self.get_request)
        self.assertContains(result, "name1", status_code=200)
        self.assertEqual(result.data[0]['name'], "name1")
        self.assertEqual(result.data[0]['procedure'], "procedure1")
        self.assertEqual([x['name'] for x in result.data[0]['ingredients']], ["ingred1", "ingred2"])
        id = result.data[0]['id']
        self.assertEqual(Recipe.objects.get(id=id).name, 'name1')

    def test_PUT(self):
        viewset = RecipeViewSet.as_view({'put': 'update'})
        put_request = self.factory.put("/recipes/", json.dumps({"name": "updatedname1", "procedure": "procedure1",
                                                           "ingredients": [{"name": "ingred1"}, {"name": "ingred3"}]}),
                                  content_type='application/json')
        viewset(put_request, pk=self.r.id)
        result = self.getviewset(self.get_request)
        self.assertContains(result, "updatedname1", status_code=200)
        self.assertEqual(result.data[0]['name'], "updatedname1")
        self.assertEqual(result.data[0]['procedure'], "procedure1")
        self.assertEqual([x['name'] for x in result.data[0]['ingredients']], ["ingred1", "ingred3"])

    def test_PATCH(self):
        viewset = RecipeViewSet.as_view({'patch': 'partial_update'})
        patch_request = self.factory.patch("/recipes/", json.dumps({"name": "updatedname2","ingredients": [{"name": "ingred4"}]}),content_type='application/json')
        viewset(patch_request, pk=self.r.id)
        result = self.getviewset(self.get_request)
        self.assertContains(result, "updatedname2", status_code=200)
        self.assertEqual(result.data[0]['name'], "updatedname2")
        self.assertEqual(result.data[0]['procedure'], "procedure1")
        self.assertEqual([x['name'] for x in result.data[0]['ingredients']], ["ingred4"])

    def test_PATCH_404(self):
        viewset = RecipeViewSet.as_view({'patch': 'partial_update'})
        patch_request = self.factory.patch("/recipes/", json.dumps({"name": "updatedname2","ingredients": [{"name": "ingred4"}]}),content_type='application/json')
        patchresponse = viewset(patch_request, pk=self.r.id+50)
        self.assertContains(patchresponse, "", status_code=404)
        result = self.getviewset(self.get_request)
        self.assertContains(result, "name1", status_code=200)
        self.assertEqual(result.data[0]['name'], "name1")
        self.assertEqual(result.data[0]['procedure'], "procedure1")
        self.assertEqual([x['name'] for x in result.data[0]['ingredients']], ["ingred1", "ingred2"])

    def test_DELETE(self):
        viewset = RecipeViewSet.as_view({'delete': 'destroy'})
        delete_request = self.factory.delete("/recipes/")
        viewset(delete_request, pk=self.r.id)
        result = self.getviewset(self.get_request)
        self.assertContains(result, "", status_code=200)
        self.assertEqual(len(result.data), 0)

        self.assertEqual(0, len(Recipe.objects.all()));

    def test_DELETE_404(self):
        viewset = RecipeViewSet.as_view({'delete': 'destroy'})
        delete_request = self.factory.delete("/recipes/")
        delresponse = viewset(delete_request, pk=self.r.id+5)
        self.assertContains(delresponse, "", status_code=404)

        result = self.getviewset(self.get_request)
        self.assertContains(result, "", status_code=200)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(1, len(Recipe.objects.all()))
