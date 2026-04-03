from women.models import Category, TagPost
from django import template
from django.db.models import Count

register = template.Library()


@register.inclusion_tag("women/list_categories.html", takes_context=True)
def show_categories(context):
    category_selected = context.get("category_selected")
    return {
        "categories": Category.objects.annotate(total=Count("posts")).filter(
            total__gt=0
        ),
        "category_selected": category_selected,
    }


@register.inclusion_tag("women/list_tags.html")
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
