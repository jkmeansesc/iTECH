from django import template
from django.template.defaultfilters import striptags

register = template.Library()


@register.filter
def first_non_empty_character(value):
    # Remove tags from content
    content_without_tags = striptags(value)
    alphanumeric_chars = []
    for char in content_without_tags:
        if char.isalnum() or char.isspace():  # If alphanumeric or space, add to result list
            alphanumeric_chars.append(char)
    if len(alphanumeric_chars) >= 40:
        # Take the first 40 characters and join with empty string
        first_three_chars = ''.join(alphanumeric_chars[:40])
    else:
        # If less than 40 characters, return all
        first_three_chars = ''.join(alphanumeric_chars)
    return first_three_chars
