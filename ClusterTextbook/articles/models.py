from django.db import models
from datetime import date

class Chapter(models.Model):
    chapter_name = models.CharField("Название главы", max_length=50)
    chapter_order = models.PositiveSmallIntegerField("Порядок главы", default=1)

    def __str__(self):
        return self.chapter_name

class Article(models.Model):
    article_name = models.CharField("Название статьи", max_length=50)
    date_of_creation = models.DateField("Дата создания", default=date.today)
    date_of_change = models.DateField("Дата последних изменений", default=date.today)
    article_order = models.PositiveSmallIntegerField("Порядок статьи", default=1)
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
    type_of_text = models.CharField("Тип текста", default="text", max_length=20, null=True)
    block_order = models.PositiveSmallIntegerField("Порядок блока", default=1)

    def __str__(self):
        return  self.text_block[:10]

class ImageBlock(models.Model):
    image_name = models.CharField()
    block_order = models.PositiveSmallIntegerField("Порядок изображения", default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", null=True)

    def __str__(self):
        return self.image_name


# Класс для сырого SQL-запроса из БД по получению текстовых
# и картиночных блоков вместе и дальнейшего их размещения на странице
class ContentBlock:
    def __init__(self, text_block, type_of_text, order_value):
        self.text_block = text_block

        # Хранит в себе либо одно из значений, либо путь к изображению в зависимости от типа контента
        self.type_of_text = type_of_text
        self.order_value = order_value

    def __str__(self):
        print(self.order_value)