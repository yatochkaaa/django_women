from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from .models import Category, TagPost, Women

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": Women.published.all(),
        "category_selected": 0,
    }
    return render(request, "women/index.html", data)


def about(request):
    data = {
        "title": "О сайте",
        "menu": menu,
    }
    return render(request, "women/about.html", data)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {"title": post.title, "menu": menu, "post": post, "category_selected": 1}
    return render(request, "women/post.html", data)


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    category_posts = Women.published.filter(category_id=category.pk)
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": category_posts,
        "category_selected": category,
    }
    return render(request, "women/index.html", data)


def show_tagpost_list(request, tagpost_slug):
    tag = get_object_or_404(TagPost, slug=tagpost_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)
    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "category_selected": None,
    }

    return render(request, "women/index.html", data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
