from unittest import TestCase

from django.contrib.sites.models import Site
from django.template import Context, Template
from django.test import RequestFactory


class FHTagTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.site, _created = Site.objects.update_or_create(pk=1, defaults={
            'domain': 'www.mysite.com'
        })

    def test_build_absolute_uri(self):
        request = RequestFactory().get('', content_type='application/json')
        context = Context({'request': request})

        template_to_render = Template(
            '{% load fh_tags %}'
            "{% build_absolute_uri path 'fb.png' as image_path %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertEqual('http://www.mysite.com/static/fb.png', context.get("image_path"))
        self.assertEqual('http://www.mysite.com/static/fb.png', rendered_template)


# class BuildAbsoluteUri(TemplateTag):
#     name = 'build_absolute_uri'
#
#     options = Options(
#         'path', Argument('path', required=True, resolve=True),
#         'as', Argument('as_var', required=False, resolve=False),
#     )
#
#     def render_tag(self, context, path=None, as_var=None):
#         request = context['request']
#         absolute_uri = request.build_absolute_uri(path)
#         if as_var:
#             context[as_var] = absolute_uri
#         return absolute_uri
