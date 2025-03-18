from django.contrib import admin
from.models import Chapter, Article, ArticleBlock, ImageBlock

class ArticleInline(admin.StackedInline):
    model = Article
    extra = 0

class ChapterAdmin(admin.ModelAdmin):
    fieldsets = [
        #(None, {"fields": ["question_text"]}),
        #("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ArticleInline]
    list_display = ["chapter_name", "chapter_order"]

admin.site.register(Chapter, ChapterAdmin)
# admin.site.register(Article)
admin.site.register(ArticleBlock)
admin.site.register(ImageBlock)
