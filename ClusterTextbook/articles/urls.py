from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path("", views.index),
    path("articles/<int:article_id>/", views.article_page, name='article_page'),
    path('articles/<int:article_id>/mark-as-read/', views.mark_article_read, name='mark_article_read'),
    path("search", views.search_article, name="search_article")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)