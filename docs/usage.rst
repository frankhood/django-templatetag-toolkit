=====
Usage
=====

To use FH Tags in a project, add it to your `INSTALLED_APPS`:

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
