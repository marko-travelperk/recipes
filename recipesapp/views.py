from recipesapp.models import Recipe
from rest_framework import viewsets
from recipesapp.serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        querysetall = Recipe.objects.all()
        queryset = querysetall

        if hasattr(self, 'request'):
            namestart = self.request.query_params.get('name', None)
            if namestart is not None:
                queryset = querysetall.filter(name__startswith=namestart)
            anyquery = self.request.query_params.get('q', None)
            if anyquery is not None and anyquery is not "":
                queryset=querysetall.filter(name__icontains=anyquery) | querysetall.filter(procedure__icontains=anyquery) | querysetall.filter(ingredients__name__icontains=anyquery)

        return queryset.distinct()
