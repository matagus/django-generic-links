# Getting started with django-generic-links

![Python Compatibility](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)
![Django Compatibility](https://img.shields.io/badge/django-4.2%20|%205.0%20|%205.1%20|%205.2-%2344B78B?labelColor=%23092E20)
[![PyPi Version](https://img.shields.io/pypi/v/django-generic-links.svg)](https://pypi.python.org/pypi/django-generic-links)
![CI badge](https://github.com/matagus/django-generic-links/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/matagus/django-generic-links/graph/badge.svg?token=a64SxEDQk0)](https://codecov.io/gh/matagus/django-generic-links)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Simple and generic application for Django projects to attach and handle links for any object. Compatible with Django 4.2 to 5.2 and Python 3.10 to 3.14.

## Features

- Model for creating generic link relations
- Reverse Generic Relation (Django) for your models
- Model Admin
- Generic inline admin to manage any model's generic links
- A template tag to get all links for a given model instance
- A fully working example project

## Installation

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

## Quick Start

Add `generic_links` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "generic_links",
    # ...
)
```

Then run the migrations:

```bash
python manage.py migrate
```

Finally, add the reverse generic relation to each of the models you're going to add generic links to:

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

## Usage

### Using django-generic-links models

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

### Generic Links Inline Admin

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

### Using django-generic-links templatetags

Now imagine you have an artist page. You're passing `artist` object using template
context and you want to get all the links for it:

```html
{% load generic_links_tags %}

<h1>{{ artist.name }}</h1>
<p>{{ artist.description }}</p>
<h2>Links for {{ artist.name }}</h2>
{% get_links_for artist as artist_links %}
<ul>
{% for link in artist_links %}
  <li><a href="{{ link.url }}" title="{{ link.title }}">{{ link.title }}</a></li>
{% endfor %}
</ul>
```

## Running Tests

**Prerequisites:** Install Hatch if not already installed: `pip install hatch`

**List available test environments:**
```bash
hatch env show test
```

**Run all tests (all Python + Django combinations):**
```bash
hatch run test:test
```

**Run tests for specific Python/Django version:**
```bash
hatch run test.py3.14-5.2:test  # Python 3.14 + Django 5.2
hatch run test.py3.13-5.1:test  # Python 3.13 + Django 5.1
```

**Run specific test file:**
```bash
hatch run test.py3.13-5.2:test tests.test_models
```

**Coverage:**
```bash
hatch run test:cov  # Run tests with coverage report
```

**Troubleshooting:** If you encounter environment issues, clean and rebuild: `hatch env prune`
