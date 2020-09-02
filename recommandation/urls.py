from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies, name="movies"),
    path('result',views.result,name="result")
]