from django.db import models


class Article(models.Model):
    article_name = models.CharField(max_length=50)

    def __str__(self):
        return self.article_name

class Article_Block(models.Model):
    text_block = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return  self.text_block[:10]