from django import template
from markdown import markdown

register = template.Library()

@register.filter(name='from_markdown')
def from_markdown(value):
	val = markdown(value, extensions=['fenced_code'])
	return val.replace("<pre>", "<pre class = \"prettyprint\">")