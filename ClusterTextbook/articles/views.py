from django.http import HttpResponse
from django.template import loader
from .models import Chapter, Article


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

def article_page(request, article_name:str):
    template = loader.get_template(f'{article_name}.html')

    # В данном случае никаких данных вставлять не нужно и контекста нет
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)