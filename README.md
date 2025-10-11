django-generic-links
====================

![Python Compatibility](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)
![Django Compatibility](https://img.shields.io/badge/django-4.2%20|%205.0%20|%205.1-%2344B78B?labelColor=%23092E20)
[![PyPi Version](https://img.shields.io/pypi/v/django-generic-links.svg)](https://pypi.python.org/pypi/django-generic-links)
![CI badge](https://github.com/matagus/django-generic-links/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/matagus/django-generic-links/graph/badge.svg?token=a64SxEDQk0)](https://codecov.io/gh/matagus/django-generic-links)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Simple app to attach links to any Django model. Compatible with Django 4.x to 5.1 and Python 3.9 to 3.14.

Features
========

- Model for creating generic link relations
- Reverse Generic Relation (Django) for your models
- Model Admin
- Generic inline admin to manage any model's generic links
- A template tag to get all links for a given model instance
- A fully working example project


Installation
============

Via `pip` command:

```bash
pip install django-generic-links
```

...or you can clone the repo and install it using `pip` too:

```bash
git clone git://github.com/matagus/django-generic-links.git
cd django-generic-links
pip install -e .
```

then add `generic_links` to your `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "generic_links",
)
```

then run the migrations:

```bash
python manage.py migrate
```

and finally add the reverse generic relation to each of the models you're going to add generic links to:

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    # This is important so that we can get the GenericLink related instances for an object of this model
    generic_links = GenericRelation("generic_links.GenericLink")


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField(null=True, blank=True)

    generic_links = GenericRelation("generic_links.GenericLink")
```


Usage
=====

Using django-generic-links models
---------------------------------

```python
>>> from generic_links.models import GenericLink
>>> from music.models import Artist
>>>
>>> # Get an artist from the database...
>>> lou_reed = Artist.objects.get(pk=1)
>>> lou_reed
<Artist: Lou Reed>
>>>
>>> # Create the first link
>>> link1 = GenericLink(title="Wikipedia Page", url="http://en.wikipedia.org/wiki/Lou_Reed", content_object=lou_reed)
>>> link1.save()
>>>
>>> # and then a second one
>>> link2 = GenericLink(title="Encyclopaedia Britannica", url="https://www.britannica.com/biography/Lou-Reed",
content_object=lou_reed)
>>> link2.save()
>>>
>>> # Now get all the links for the artist object:
>>> lou_reed.generic_links.all()
<QuerySet [<GenericLink: Encyclopaedia Britannica :: https://www.britannica.com/biography/Lou-Reed>,
<GenericLink: Wikipedia Page :: https://en.wikipedia.org/wiki/Lou_Reed>]>
```

Generic Links Inline Admin
--------------------------

Since a `GenericLink` instance will be associated to another object you usually
wish to show an inline model admin form in that model form.

```python
from django.contrib import admin

from generic_links.admin import GenericLinkStackedInline

from music_app.models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    # ...
    inlines = [GenericLinkStackedInline]
```


Using django-generic-links templatetags
---------------------------------------

Now imagine you have an artist page. You're passing `artist` object using template
context and you want to get all the links for it:

```html
{% load generic_links_tags %}

<hl>{{ artist.name }}</hl>
<p>{{ artist.description }}</p>
<h2>Links for {{ artist.name }}</h2>
{% get_links_for artist as artist_links %}
<ul>
{% for link in artist_links %}
  <li><a href="{{ link.url }}" title="{{ link.title }}">{{ link.title }}</a></li>
{% endfor %}
</ul>
```


Contributing
============

Contributions are welcome! ❤️

Please read [Contributing.md](CONTRIBUTING.md) for detailed instructions on how to help.

Running Tests
-------------

`hatch run test:test` will run the tests in every Python + Django versions combination.

`hatch run test.py3.13-5.1:test` will run them for python 3.13 and Django 5.1. Please see possible combinations using
`hatch env show` ("test" matrix).


License
=======

`django-generic-links` is released under a BSD License - see the `LICENSE` file
for more information.


Acknowledgements
================

Develop & built using [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tools used in building this package:

-   [Cookiecutter](https://github.com/audreyr/cookiecutter) and [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage) for rendering this package.

Posts I learned from:

- [Switching to Hatch](https://andrich.me/2023/08/switching-to-hatch/)
- [Automate Hatch Publish with GitHub Actions](https://blog.pecar.me/automate-hatch-publish)
