from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("articles/<int:article_id>/", views.article_page, name='article_page'),
    path('articles/<int:article_id>/mark-as-read/', views.mark_article_read, name='mark_article_read'),
    path("search", views.search_article, name="search_article")
]