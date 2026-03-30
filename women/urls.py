from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.addpage, name="add_page"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login, name="login"),
    path("post/<slug:post_slug>/", views.show_post, name="post"),
    path("category/<slug:category_slug>/", views.show_category, name="category"),
    path("tag/<slug:tagpost_slug>/", views.show_tagpost_list, name="tag"),
]
