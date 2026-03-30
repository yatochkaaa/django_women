from women.models import Category, TagPost
from django import template

register = template.Library()


@register.inclusion_tag("women/list_categories.html", takes_context=True)
def show_categories(context):
    category_selected = context.get("category_selected")
    return {
        "categories": Category.objects.all(),
        "category_selected": category_selected,
    }


@register.inclusion_tag("women/list_tags.html")
def show_all_tags():
    return {"tags": TagPost.objects.all()}
