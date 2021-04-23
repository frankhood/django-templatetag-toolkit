=============================
FH Tags
=============================

.. image:: https://badge.fury.io/py/fh-tags.svg
    :target: https://badge.fury.io/py/fh-tags

.. image:: https://travis-ci.org/frankhood/fh-tags.svg?branch=master
    :target: https://travis-ci.org/frankhood/fh-tags

.. image:: https://codecov.io/gh/frankhood/fh-tags/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/fh-tags

Your project description goes here

Documentation
-------------

The full documentation is at https://fh-tags.readthedocs.io.

Quickstart
----------

Install FH Tags::

    pip install fh-tags

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'fh_tags.apps.FhTagsConfig',
        ...
    )

Add FH Tags's URL patterns:

.. code-block:: python

    from fh_tags import urls as fh_tags_urls


    urlpatterns = [
        ...
        url(r'^', include(fh_tags_urls)),
        ...
    ]

Features
--------

* TODO

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
