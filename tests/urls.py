# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="test.html")),
]
