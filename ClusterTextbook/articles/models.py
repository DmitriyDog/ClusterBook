from django.db import models
from datetime import date

class Chapter(models.Model):
    chapter_name = models.CharField(max_length=50)
    chapter_order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.chapter_name

class Article(models.Model):
    article_name = models.CharField(max_length=50)
    date_of_creation = models.DateField("Дата создания", default=date.today)
    date_of_change = models.DateField("Дата последних изменений", default=date.today)
    article_order = models.PositiveSmallIntegerField(default=1)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.article_name

class ArticleBlock(models.Model):
    text_block = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    '''
    Типы текста:
    text - простой абзац с текстом
    code - код
    header - заголовок
    '''
    type_of_text = models.CharField(default="text", max_length=20, null=True)
    block_order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return  self.text_block[:10]

class ImageBlock(models.Model):
    image_name = models.CharField()
    image_order = models.PositiveSmallIntegerField(default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.image_name
