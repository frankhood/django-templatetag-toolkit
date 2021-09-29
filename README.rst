=============================
Django Templatetag Toolkit
=============================

.. image:: https://badge.fury.io/py/django_templatetag_toolkit.svg
    :target: https://badge.fury.io/py/django-templatetag-toolkit

.. image:: https://travis-ci.org/frankhood/django_templatetag_toolkit.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-templatetag-toolkit

.. image:: https://codecov.io/gh/frankhood/django_templatetag_toolkit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-templatetag-toolkit



Documentation
-------------

The full documentation is at https://github.com/frankhood/django-templatetag-toolkit/tree/main/docs

Quickstart
----------

Install Django Templatetag Toolkit::

    pip install django-templatetag-toolkit

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django-templatetag-toolkit',
        ...
    )


Features
--------

* annotate_form_field
* BuildAbsoluteUri
* GenericEntryListWidget
* GetListWidget
* GetDictWidget
* RemoveBreak
* easy_tag
* append_to_get
* change_language

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
