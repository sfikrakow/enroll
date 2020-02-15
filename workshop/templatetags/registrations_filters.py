from django import template

register = template.Library()


@register.filter
def first_name(data, field_name):
    return data[int(field_name[4:])]['registration'].participant.first_name


@register.filter
def last_name(data, field_name):
    return data[int(field_name[4:])]['registration'].participant.last_name


@register.filter
def answers(data, field_name):
    return data[int(field_name[4:])]['answers']


@register.filter
def auto_response(data, field_name):
    return data[int(field_name[4:])]['registration'].workshop.auto_response
