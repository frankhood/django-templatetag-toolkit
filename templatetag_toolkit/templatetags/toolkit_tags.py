""" django-templatetag-toolkit.templatetags.templatetag_toolkit.py by Frankhood
    @author: Frankhood Business Solutions
"""

import logging
import re

from classytags.arguments import Argument
from classytags.core import Options
from classytags.core import Tag as TemplateTag
from classytags.exceptions import ArgumentRequiredError
from django import template
from django.apps.registry import apps
from django.db import models
from django.template.base import TemplateSyntaxError
from django.template.context import Context
from django.template.loader import render_to_string
from django.urls import translate_url

logger = logging.getLogger("django-templatetag-toolkit")

register = template.Library()


@register.tag
def annotate_form_field(parser, token):
    """
    Set an attribute on a form field with the widget type

    This means templates can use the widget type to render things differently
    if they want to.  Django doesn't make this available by default.

    Usage:
    {% annotate_form_field my_field %}

    {% if my_field.widget_type == 'CheckboxInput' %}
        {% include 'partials/form_field_checkbox.html' with field=my_field %}
    {% elif my_field.widget_type == 'RadioInput' %}
        {% include 'partials/form_field_radio.html' with field=my_field %}
    {% else %}
        {% include 'partials/form_field.html' with field=my_field %}
    {% endif %}
    """

    class FormFieldNode(template.Node):
        def __init__(self, field_str):
            self.field = template.Variable(field_str)

        def render(self, context):
            field = self.field.resolve(context)
            if hasattr(field, "field"):
                field.widget_type = field.field.widget.__class__.__name__
            return ""

    args = token.split_contents()
    if len(args) < 2:
        raise TemplateSyntaxError(
            "annotate_form_field tag requires a form field to be passed"
        )
    return FormFieldNode(args[1])


@register.tag("build_absolute_uri")
class BuildAbsoluteUri(TemplateTag):
    name = "build_absolute_uri"

    options = Options(
        "path",
        Argument("path", required=True, resolve=True),
        "as",
        Argument("as_var", required=False, resolve=False),
    )

    def render_tag(self, context, path=None, as_var=None):
        request = context["request"]
        absolute_uri = request.build_absolute_uri(path)
        if as_var:
            context[as_var] = absolute_uri
        return absolute_uri


# register.tag(BuildAbsoluteUri)


class GenericEntryListWidget(TemplateTag):
    """example:
    {% show_elements_list 'app.Model' with_manager 'published_objects' filter_by 'foo=baz' limit '5' order_by 'order using 'foopath/template.html' as my_object_list %}
    """

    name = "show_elements_list"

    options = Options(
        Argument("model", required=True, resolve=True),
        "with_manager",
        Argument("model_manager", required=False, resolve=False),
        "filter_by",
        Argument("filter_by", required=False, resolve=False),
        "limit",
        Argument("limit", required=False, resolve=False),
        "order_by",
        Argument("order_by", required=False, resolve=False),
        "using",
        Argument("template", required=False, resolve=False),
        "as",
        Argument("varname", required=False, resolve=False),
    )

    def render_tag(
        self,
        context,
        model,
        model_manager,
        filter_by,
        limit,
        template,
        order_by,
        varname,
    ):  # noqa
        try:
            if issubclass(model.__class__, models.Model):
                Model = model.__class__
            else:
                Model = apps.get_model(model)
        except LookupError:
            logger.exception(
                f"Model '{model}' not found with using template tag show_elements_list"
            )
        if not model_manager:
            model_manager = "objects"
        filter_kwargs = (
            dict(([x.__str__() for x in filter_by.split("=")],)) if filter_by else {}
        )
        entry_qs = getattr(Model, model_manager).filter(**filter_kwargs)
        if order_by:
            entry_qs = entry_qs.order_by(*order_by.split(","))
        if limit:
            entry_qs = entry_qs[: int(limit)]
        # logger.info("enrty qs: {0}".format([x.__unicode__() for x in entry_qs]))
        # logger.info("enrty qs count: {0}".format(entry_qs.count()))
        if varname:
            context.update(
                {
                    varname: entry_qs,
                }
            )
            return ""
        elif template:
            tag_context = Context(
                {"object_list": entry_qs, "request": context.get("request")}
            )
            html_output = render_to_string(template, tag_context)
            return html_output
        else:
            raise ArgumentRequiredError(
                "show_elements_list requires at least one attribute between template and varname to work properly"
            )


register.tag(GenericEntryListWidget)


class GetListWidget(TemplateTag):
    """example:
    {% get_list '1, x ,fuffa' as my_list %}
    {% for item in my_list %}
        {{forloop.counter}}.{{item}}
    {% endfor %}
    """

    name = "get_list"

    options = Options(
        Argument("values", required=True, resolve=False),
        "as",
        Argument("varname", required=True, resolve=False),
    )

    def render_tag(self, context, values, varname):
        custom_list = [x.strip() for x in values.split(",")]
        if varname:
            context.update(
                {
                    varname: custom_list,
                }
            )
            return ""
        else:
            raise ArgumentRequiredError(
                "show_elements_list requires at least one attribute between template and varname to work properly"
            )


register.tag(GetListWidget)


class GetDictWidget(TemplateTag):
    """example:
    {% get_dict 'x=1 , y=2, z=3' as my_dict %}
    {% for k,v in my_dict.items %}
        {{k}} = {{v}}
    {% endfor %}
    """

    name = "get_dict"

    options = Options(
        Argument("values", required=True, resolve=False),
        "as",
        Argument("varname", required=True, resolve=False),
    )

    def render_tag(self, context, values, varname):
        from collections import OrderedDict

        dict_list = [x.strip() for x in values.split(",")]
        custom_dict = OrderedDict()
        for d in dict_list:
            k, v = d.split("=")
            custom_dict.update({k: v})
        if varname:
            context.update(
                {
                    varname: custom_dict,
                }
            )
            return ""
        else:
            raise ArgumentRequiredError(
                "show_elements_list requires at least one attribute between template and varname to work properly"
            )


register.tag(GetDictWidget)


class RemoveBreak(TemplateTag):
    name = "removebreak"
    options = Options(
        blocks=[("endremovebreak", "body")],
    )

    def render_tag(self, context, body):
        output = body.render(context).replace("\n", " ")
        output = re.sub(r"\s+", " ", output)
        return output


register.tag(RemoveBreak)


# From here : http://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code
@register.tag
def setvar(parser, token):
    # This version uses a regular expression to parse tag contents.
    class SetVarNode(template.Node):
        def __init__(self, new_val, var_name):
            self.new_val = new_val
            self.var_name = var_name

        def render(self, context):
            context[self.var_name] = self.new_val
            return ""

    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0]
        )
    m = re.search(r"(.*?) as (\w+)", arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    new_val, var_name = m.groups()
    if not (new_val[0] == new_val[-1] and new_val[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return SetVarNode(new_val[1:-1], var_name)


# Decorator to facilitate template tag creation
def easy_tag(func):
    """deal with the repetitive parts of parsing template tags"""

    def inner(parser, token):
        # print token
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError(
                'Bad arguments for tag "%s"' % token.split_contents()[0]
            )

    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner


@register.tag()
@easy_tag
def append_to_get(_tag_name, dict):
    class AppendGetNode(template.Node):
        """
        takenFrom https://djangosnippets.org/snippets/1627/
        example usage :
        {% for page_num in results.paginator.page_range %}
        <a href="{% append_to_get p=page_num %}">{{ page_num }}</a>
        {% endfor %}
        """

        def __init__(self, dict):
            self.dict_pairs = {}
            for pair in dict.split(","):
                pair = pair.split("=")
                self.dict_pairs[pair[0]] = template.Variable(pair[1])

        def render(self, context):
            get = context["request"].GET.copy()
            logger.info(f"get pre: {get}")
            for key in self.dict_pairs:
                get[key] = self.dict_pairs[key].resolve(context)
                logger.info(f"get[{key}] : {get[key]}")

            path = context["request"].META["PATH_INFO"]
            logger.info(f"path : {path}")
            logger.info(f"get post: {get}")

            if len(get):
                path += "?%s" % "&".join(
                    [
                        f"{key}={value}"
                        for (key, value) in get.items()
                        if (value != "" and value is not None)
                    ]
                )
            return path

    return AppendGetNode(dict)


@register.simple_tag(takes_context=True)
def change_language(context, lang=None, *args, **kwargs):
    path = context["request"].path
    return translate_url(path, lang)
