from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Template tag for adding CSS class to field."""
    return field.as_widget(attrs={'class': css})
