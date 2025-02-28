from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("articles/<int:article_id>/", views.article_page, name='article_page')
]