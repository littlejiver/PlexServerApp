from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('result/dbsearch/', views.search_database, name='dbsearch'),
    path('result/dbsearch/progress_bar/', views.progress_bar, name='progress_bar')
]
