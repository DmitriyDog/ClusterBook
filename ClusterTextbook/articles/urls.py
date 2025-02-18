from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("articles/<str:article_name>/", views.article_page, name='article_page')
]