from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'polls', views.PollsViewSet)

urlpatterns = [
    path('', views.index, name='index'),
]