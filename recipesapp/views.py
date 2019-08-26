from recipesapp.models import Recipe, Ingredient
from rest_framework import viewsets
from recipesapp.serializers import IngredientSerializer, RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        namestart = self.request.query_params.get('name', None)
        if namestart is not None:
            queryset = queryset.filter(name__startswith=namestart)
        return queryset
