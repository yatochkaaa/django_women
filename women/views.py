from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from .forms import AddPostForm, ContactForm
from .utils import DataMixin
from .models import Category, TagPost, Women


class WomenHome(DataMixin, ListView):
    """Display the home page with a list of published women posts."""

    template_name = "women/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    category_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related("category")


@login_required
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "women/about.html", {"title": "О сайте", "page_obj": page_obj}
    )


class ShowPost(DataMixin, DetailView):
    template_name = "women/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    title_page = "Добавление статьи"
    permission_required = "women.add_women"

    def form_valid(self, form):
        data = form.save(commit=False)
        data.author = self.request.user
        return super().form_valid(form)

    # <FormView code>
    # form_class = AddPostForm
    # success_url = reverse_lazy("home")

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "category"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"
    permission_required = "women.change_women"


class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Удаление статьи"


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    template_name = "women/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


# def contact(request):
#     return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(
            category__slug=self.kwargs["category_slug"]
        ).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context["posts"][0].category
        return self.get_mixin_context(
            context,
            title=f"Категория - {category.name}",
            category_selected=category.slug,
        )


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    category_posts = Women.published.filter(category_id=category.pk).select_related(
        "category"
    )
    data = {
        "title": f"Рубрика: {category.name}",
        "posts": category_posts,
        "category_selected": category,
    }
    return render(request, "women/index.html", data)


class ShowTagPostList(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs["tagpost_slug"]
        ).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs["tagpost_slug"])
        return self.get_mixin_context(context, title=f"Тег: {tag.tag}")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
