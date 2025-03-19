from django.contrib import admin
from.models import Chapter, Article, ArticleBlock, ImageBlock

class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0
    fields = ["article_name", "article_order", "date_of_creation", "date_of_change"]    # порядок полей при изменении
    ordering = ["article_order"]
    search_fields = ["article_name"]

class ChapterAdmin(admin.ModelAdmin):
    list_display = ["chapter_name", "chapter_order"]    # уже будет видно до редактирования глав
    ordering = ["chapter_order"]
    search_fields = ["chapter_name"]
    inlines = [ArticleInline]                           # вместе с главами можно сразу редактировать статьи к ним

class ArticleBlockInLine(admin.TabularInline):
    model = ArticleBlock
    extra = 0
    ordering = ["block_order"]

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["article_name", "article_order", "chapter"]    # уже будет видно до редактирования глав
    ordering = ["chapter", "article_order"]
    fields = [("article_name", "article_order", "chapter"), ("date_of_creation", "date_of_change")]
    search_fields = ["article_name"]
    inlines = [ArticleBlockInLine]

admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Article, ArticleAdmin)
# admin.site.register(ArticleBlock)
# admin.site.register(ImageBlock)
