from django.http import HttpResponse
from django.template import loader
from .models import Chapter, Article, ArticleBlock, ImageBlock
from .forms import ReadArticleForm
from django.core.cache import cache
from django.shortcuts import redirect
from .side_algorithms.kmp import KMPSearch
from django.http import JsonResponse


def index(request):
    # Создаётся шаблон на основе странички
    template = loader.get_template('index.html')

    # Получаю список всех глав, сортирую по номеру и заранее загружаю связанные с ними статьи через prefetch_related
    chapter_list = Chapter.objects.order_by("chapter_order").prefetch_related("article_set")
    # Это данные, которые нужно подставить в шаблон.
    cache_list = [article.pk for article in Article.objects.all() if cache.get(f"article_{article.pk}_read")]
    context = {
        "chapter_list": chapter_list,
        "cache_list": cache_list
    }

    # Шаблон превращается в “отрендеренную страницу” после того, как туда подставлены данные.
    rendered_page = template.render(context, request)
    # Возвращаем отрендеренную страницу
    return HttpResponse(rendered_page)


def article_page(request, article_id:int):
    template = loader.get_template('article-page.html')

    chapter_list = Chapter.objects.order_by("chapter_order").prefetch_related("article_set")
    opened_article = Article.objects.get(pk=article_id)
    article_content = ArticleBlock.objects.filter(article=opened_article).order_by("block_order")
    header_list = article_content.filter(type_of_text="header")
    next_article = (Article.objects.filter(article_order__gt=opened_article.article_order)
                    .order_by("article_order").first())
    previous_article = (Article.objects.filter(article_order__lt=opened_article.article_order)
                        .order_by("-article_order").first())
    cache_list = [article.pk for article in Article.objects.all() if cache.get(f"article_{article.pk}_read")]

    context = {
        "chapter_list": chapter_list,
        "article_content": article_content,
        "article_header": opened_article.article_name,
        "header_list": header_list,
        "next_article": next_article,
        "previous_article": previous_article,
        "read_form": ReadArticleForm,
        "article_pk": opened_article.id,
        "is_article_read": cache.get(f"article_{article_id}_read"),
        "cache_list": cache_list
    }
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def mark_article_read(request, article_id: int):
    if request.method == "POST":
        # Проверяем, существует ли статья с таким ID
        try:
            article = Article.objects.get(pk=article_id)
        except Article is None:
            return HttpResponse("Статья не найдена", status=404)

        current_state = cache.get(f"article_{article_id}_read")

        if current_state is None or not current_state:
            # Отмечаем прочитанную статью в кэше
            cache.set(f"article_{article_id}_read", True, timeout=None)
        else:
            # Если статья уже помечена как прочитанная, снимаем отметку
            cache.delete(f"article_{article_id}_read")

    return redirect(f"/articles/{article_id}/")


'''
Релевантность результата зависит от того, где встречается искомая строка:
Название статьи = 1000 очков
Подзаголовок статьи = 200 очков
Текст статьи = 1 очко
'''
def search_article(request):
    if request.method == "POST":
        search_query = request.POST.get("q", "")
        if search_query:
            # Поиск
            article_list = Article.objects.prefetch_related("articleblock_set").all()

            # В качестве результата выдается 3 лучших (релевантных) статьи, которые набрали наибольшее количество очков
            score_count = []
            for article in article_list:
                score = 0

                # Использую алгоритм Кнута — Морриса — Пратта для поиска подстроки
                score += len(KMPSearch(search_query, article.article_name)) * 1000
                header_list = article.articleblock_set.filter(type_of_text="header")
                text_list = article.articleblock_set.filter(type_of_text="text")
                for header in header_list:
                    score += len(KMPSearch(search_query, header.text_block)) * 200
                for paragraph in text_list:
                    score += len(KMPSearch(search_query, paragraph.text_block))
                if score_count and len(score_count) == 3 and score > score_count[-1][-1]:
                        score_count[-1] = (article.pk, article.article_name, score)
                elif score != 0:
                    score_count.append((article.pk, article.article_name, score))
                score_count.sort(key=lambda x: x[-1], reverse=True)
            if score_count:
                context = {"search_results": [{
                    "article_name": elem[1],
                    "pk": elem[0]
                } for elem in score_count]}
            else:
                context = {}
        else:
            context = {}
        return JsonResponse(context)
    return HttpResponse("Произошла ошибка на стороне сайта", status=404)
