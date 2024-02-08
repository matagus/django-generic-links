django-generic-links
====================

![Python Compatibility](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg) [![PyPi Version](https://img.shields.io/pypi/v/django-generic-links.svg)](https://pypi.python.org/pypi/django-generic-links)  ![CI badge](https://github.com/matagus/django-generic-links/actions/workflows/ci.yml/badge.svg) [![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Simple app to attach links to any Django model. Compatible with Django 4.x to 5.0 and Python 3.9 to 3.12.

![](docs/images/admin.png)


Features
========

- Model Admin
- Generic inline admin
- A template tag to get all links for a given model instance


Installation
============

Installing `django-generic-links` is fairly easy. You can...

    pip install django-generic-links

...or, you can clone the repo and install it the old fashioned way.

    git clone git://github.com/matagus/django-generic-links.git
    cd django-generic-links
    pip install -e .

then add `generic_links` to your `settings.py`:

``` python
INSTALLED_APPS = (
    # ...
    "generic_links",
)
```

and then run the migrations!

    # python manage.py migrate


Usage
=====

Using django-generic-links models
---------------------------------

Imagine you have a music app in your project where you save and manage artist's data. So you have an `Artist model`.
And you'd like to store and display links for each artist, say her facebook page, her youtube artist page and her
last.fm profile page:

![](docs/images/usage.png)


Generic Links Inline Admin
--------------------------

Since a `GenericLink` instance will be associated to another object you usually
wish to show an inline model admin form in that model form.

![](docs/images/inline.png)


Using django-generic-links templatetags
---------------------------------------

Now imagine you have an artist page. You're passing `artist` object using template
context and you want to get all the links for it:

![](docs/images/templatetags.png)

Development / Contributions
===========================

Running Tests
-------------

`hatch run test:test` will run the tests in every Python + Django versions combination.


Development commands
--------------------

`hatch shell`


Want to help?
-------------

If you'd like to help, write example code, contribute patches, document things
on the wiki your help is always appreciated! Just fork the project, clone your
repo, commit, push and send me a pull request


License
=======

`django-generic-links` is released under an BSD License - see the `LICENSE` file
for more information.


Acknowledgements
================

Develop & built using [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tools used in building this package:

-   [Cookiecutter](https://github.com/audreyr/cookiecutter) and [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage) for rendering this package.
-   [Carbon](https://carbon.now.sh/) for those beautiful code snippets.

Posts I learned from:

- [Switching to Hatch](https://andrich.me/2023/08/switching-to-hatch/)
