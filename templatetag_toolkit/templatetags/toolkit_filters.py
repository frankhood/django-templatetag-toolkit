""" django-templatetag-toolkit.templatetags.utils.py by Frankhood
    @author: Frankhood Business Solutions
"""

import json
import os
import re

from django import template
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.template.defaultfilters import stringfilter
from django.utils.html import escape, strip_tags
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def autolink(text):
    url_regexp = re.compile(
        r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|([a-z0-9.\-]+[.][a-z]{2,4}/))(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))"""
    )
    starting = 0
    while True:
        has_matched = url_regexp.search(text, starting)
        if has_matched:
            link = '<a href="{msg}" target="_blank">{msg}</a>'.format(
                msg=has_matched.group(0)
            )
            text = text[: has_matched.start(0)] + link + text[has_matched.end(0) :]
            starting = has_matched.start(0) + len(link)
        else:
            break
    return text


@register.filter
def keeptags(value, tags):
    """
    Strips all [X]HTML tags except the space seperated list of tags
    from the output.

    Usage: keeptags:"strong em ul li"
    """
    tags = [re.escape(tag) for tag in tags.split()]
    tags_re = "(%s)" % "|".join(tags)
    singletag_re = re.compile(r"<(%s\s*/?)>" % tags_re)
    starttag_re = re.compile(r"<(%s)(\s+[^>]+)>" % tags_re)
    endtag_re = re.compile(r"<(/%s)>" % tags_re)
    value = singletag_re.sub(r"##~~~\g<1>~~~##", value)
    value = starttag_re.sub(r"##~~~\g<1>\g<3>~~~##", value)
    value = endtag_re.sub(r"##~~~\g<1>~~~##", value)
    value = strip_tags(value)
    value = escape(value)
    recreate_re = re.compile("##~~~([^~]+)~~~##")
    value = recreate_re.sub(r"<\g<1>>", value)
    return value


@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
    <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
    <li>0. Do something</li>
    <li>1. Do something</li>
    <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)


@register.filter(name="subtract")
def subtract(value, arg):
    """
    Similar to |add:"-5" but what if 5 is a variable?
    {% with limit = 5 %}
    + {{mymodel.objects.count|subtract:limit}} items
    {% endwith %}
    """
    return int(value) - int(arg)


@register.filter
def jsonify(obj):
    """
    Based on less-supported django-jsonify
    https://bitbucket.org/marltu/django-jsonify
    usage: {{ your_custom_queryset|jsonify}}
    n.b. do not wrap it in '' or ""

    """
    if isinstance(obj, QuerySet):
        return mark_safe(serialize("json", obj))
    return mark_safe(json.dumps(obj, cls=DjangoJSONEncoder))


@register.filter(name="escape")
@stringfilter
def escape_tag(s):
    """
    Returns the given text with ampersands, quotes and angle brackets encoded
    for use in HTML.

    ex.
    {{ text|escape }}
    """
    return escape(s)


@register.filter
def split(value, arg):
    return value.split(arg)


@register.filter
def filename(value):
    if value and value.file:
        return os.path.basename(value.file.name)
    return ""
