from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from .models import Category, TagPost, UploadFiles, Women
from .forms import AddPostForm, UploadFileForm

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
        "posts": Women.published.all().select_related("category"),
        "category_selected": 0,
    }
    return render(request, "women/index.html", data)


# def handle_uploaded_file(f):
#     file_name = str(int(datetime.timestamp(datetime.now()))) + "." + f.name.split(".")[1]
#     with open(f"uploads/{file_name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data["file"])
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()

    data = {
        "form": form,
        "title": "О сайте",
        "menu": menu,
    }

    return render(request, "women/about.html", data)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {"title": post.title, "menu": menu, "post": post, "category_selected": 1}
    return render(request, "women/post.html", data)


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
        #     try:
        #         Women.objects.create(**form.cleaned_data)
        #         return redirect("home")
        #     except Exception:
        #         form.add_error(None, "Ошибка добавления поста")
    else:
        form = AddPostForm()

    data = {
        "form": form,
        "title": "Добавление статьи",
        "menu": menu,
    }
    return render(request, "women/addpage.html", data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    category_posts = Women.published.filter(category_id=category.pk).select_related(
        "category"
    )
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": category_posts,
        "category_selected": category,
    }
    return render(request, "women/index.html", data)


def show_tagpost_list(request, tagpost_slug):
    tag = get_object_or_404(TagPost, slug=tagpost_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related(
        "category"
    )
    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "category_selected": None,
    }

    return render(request, "women/index.html", data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
