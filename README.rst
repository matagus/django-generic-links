=============================
django-generic-links
=============================

Simple and generic application for Django projects to attach and handle links for any object

Documentation
-------------

The full documentation is at https://matagus.alameda.dev/django-generic-links/.

Quickstart
----------

Install django-generic-links::

    pip install generic_links

Add it to your `INSTALLED_APPS`:

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
