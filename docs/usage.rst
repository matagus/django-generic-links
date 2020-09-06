=====
Usage
=====

To use django-generic-links in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'generic_links.apps.GenericLinksConfig',
        ...
    )

Add django-generic-links's URL patterns:

.. code-block:: python

    from generic_links import urls as generic_links_urls


    urlpatterns = [
        ...
        url(r'^', include(generic_links_urls)),
        ...
    ]
