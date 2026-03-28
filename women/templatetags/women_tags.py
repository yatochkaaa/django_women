from django import template
import women.views as views

register = template.Library()


@register.simple_tag(name="get_categories")
def get_categories():
    return views.categories_db


@register.inclusion_tag("women/list_categories.html", takes_context=True)
def show_categories(context):
    category_selected = context.get("category_selected", 0)
    categories = views.categories_db
    return {"categories": categories, "category_selected": category_selected}
