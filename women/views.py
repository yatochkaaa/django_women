from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from .models import Women

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]

categories_db = [
    {"id": 1, "name": "Актрисы"},
    {"id": 2, "name": "Певицы"},
    {"id": 3, "name": "Спортсменки"},
]


def index(request):
    posts = Women.published.all()
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
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


def show_category(request, category_id):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": data_db,
        "category_selected": category_id,
    }
    return render(request, "women/index.html", data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
