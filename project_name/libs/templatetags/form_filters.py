from django import template
from django.forms.forms import BoundField
from django.template import Context
from django.template.loader import get_template


register = template.Library()


@register.filter
def as_semantic(form, exclude_fields=""):
    """
    @option exclude contains field names comma separated
    """
    template = get_template("partials/form.html")
    c = Context({
        "form": form,
        "exclude_fields": exclude_fields.split(',') if exclude_fields else None
    })
    return template.render(c)

@register.filter
def css_class(field):
    if isinstance(field, BoundField):
        field = field.field
    return field.widget.__class__.__name__.lower()

@register.filter
def is_disabled(field):
    if isinstance(field, BoundField):
        field = field.field
    return 'disabled' in field.widget.attrs

@register.filter
def is_readonly(field):
    if isinstance(field, BoundField):
        field = field.field
    return ('readonly' in field.widget.attrs 
        and field.widget.attrs.get('readonly') is True)
