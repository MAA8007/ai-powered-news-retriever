# articles/templatetags/bookmark_tags.py

from django import template
from ..models import Bookmark

register = template.Library()

@register.filter
def is_bookmarked(article, user):
    return Bookmark.objects.filter(article=article, user=user).exists()
