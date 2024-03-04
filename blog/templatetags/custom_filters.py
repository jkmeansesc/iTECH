from django import template
from django.template.defaultfilters import striptags

register = template.Library()


@register.filter
def first_non_empty_character(value):
    content_without_tags = striptags(value)
    alphanumeric_chars = []
    for char in content_without_tags:
        if char.isalnum() or char.isspace():  # 如果是字母、数字或空格，则加入结果列表
            alphanumeric_chars.append(char)
    if len(alphanumeric_chars) >= 40:
        first_three_chars = ''.join(alphanumeric_chars[:40])  # 取前三个字符并以空字符串连接
    else:
        first_three_chars = ''.join(alphanumeric_chars)  # 如果不足三个字符，则返回全部
    return first_three_chars
