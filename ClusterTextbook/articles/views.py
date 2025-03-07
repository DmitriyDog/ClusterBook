from django.http import HttpResponse
from django.template import loader
from .models import Chapter, Article, ArticleBlock, ImageBlock


def index(request):
    # Создаётся шаблон на основе странички
    template = loader.get_template('index.html')

    # Получаю список всех глав, сортирую по номеру и заранее загружаю связанные с ними статьи через prefetch_related
    chapter_list = Chapter.objects.order_by("chapter_order").prefetch_related("article_set")
    # Это данные, которые нужно подставить в шаблон.
    context = {
        "chapter_list": chapter_list
    }

    # Шаблон превращается в “отрендеренную страницу” после того, как туда подставлены данные.
    rendered_page = template.render(context, request)
    # Возвращаем отрендеренную страницу
    return HttpResponse(rendered_page)

def article_page(request, article_id:int):
    #template = loader.get_template(f'{article_id}.html')
    template = loader.get_template('article-page.html')

    chapter_list = Chapter.objects.order_by("chapter_order").prefetch_related("article_set")
    opened_article = Article.objects.get(pk=article_id)
    article_content = ArticleBlock.objects.filter(article=opened_article).order_by("block_order")
    header_list = article_content.filter(type_of_text="header")
    context = {
        "chapter_list": chapter_list,
        "article_content": article_content,
        "article_header": opened_article.article_name,
        "header_list": header_list
    }
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)