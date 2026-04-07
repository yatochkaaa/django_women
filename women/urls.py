from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path("", views.WomenHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login, name="login"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path(
        "category/<slug:category_slug>/", views.WomenCategory.as_view(), name="category"
    ),
    path("tag/<slug:tagpost_slug>/", views.ShowTagPostList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit_page"),
    path("delete/<slug:slug>/", views.DeletePage.as_view(), name="delete_page"),
]
