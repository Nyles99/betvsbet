from django import template
from tour.models import Category, TagPost
import tour.views as views


register = template.Library()


@register.inclusion_tag('tour/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('tour/list_tags.html')
def show_all_tags():
    cats = Category.objects.all()
    return {'tags': TagPost.objects.all()}