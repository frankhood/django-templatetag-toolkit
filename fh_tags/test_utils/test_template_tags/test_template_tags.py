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

    def test_change_language(self):
        request = RequestFactory().get('/testo/', content_type='application/json')
        context = Context({'request': request})
        template_to_render = Template(
            '{% load fh_tags %}'
            "{% change_language 'en' %}"
        )
        rendered_template = template_to_render.render(context)
        print(rendered_template)
        # self.assertEqual('http://www.mysite.com/static/test/fb.png', rendered_template)

# def change_language(context, lang=None, *args, **kwargs):
#     path = context['request'].path
#     return translate_url(path, lang)
