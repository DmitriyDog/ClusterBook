from django.http import HttpResponse
from django.template import loader


def index(request):
    # Создаётся шаблон на основе странички
    template = loader.get_template('index.html')

    # Это данные, которые нужно подставить в шаблон.
    # В этой конкретной ситуации данные туда подставлять не нужно, поэтому словарь остаётся пустым.
    context = {}

    # Шаблон превращается в “отрендеренную страницу” после того, как туда подставлены данные.
    rendered_page = template.render(context, request)
    # Возвращаем отрендеренную страницу
    return HttpResponse(rendered_page)

def article_page(request, article_name:str):
    template = loader.get_template(f'{article_name}.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)