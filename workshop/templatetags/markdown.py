import markdown
from django import template

register = template.Library()


@register.filter
def markdownify(text):
    return markdown.markdown(text, output_format='html5')
