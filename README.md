django-generic-links - Attach links to any Django model
================================================================================

The latest version of django-generic-links requires Django >= 1.8. If you want
to use it with Dajngo < 1.8 please install a 0.3.x version.

Installation
--------------------------------------------------------------------------------
Installing `django-generic-links` is fairly easy. You can...

    (pip install | easy_install) django-generic-links

...or, you can clone the repo and install it the old fashioned way.

    git clone git://github.com/matagus/django-generic-links.git
    cd django-generic-links
    sudo python setup.py install

then add `generic_links` to your `settings.py`:

``` python
    INSTALLED_APPS = (
        # ...
        'generic_links',
    )
```

and then run the migrations!

    # python manage.py migrate


Using django-generic-links models
--------------------------------------------------------------------------------
Guess you have a music app in your project where you store Artist data. And you
would like to store and display links for each artist, say his facebook page,
his last.fm profile, his youtube artist page and the like:

``` python
>>> from generic_links.models import GenericLink
>>> from music.models import Artist
>>> lou_reed = Artist.objects.get(pk=1)
>>> lou_reed
<Artist: Lou Reed>

>>> link1 = GenericLink()
>>> link1.title = "Wikipedia Page"
>>> link1.url = "http://en.wikipedia.org/wiki/Lou_Reed"
>>> link1.is_external = True
>>> link1.content_object = lour_reed
>>> link1.save()

>>> link2 = GenericLink()
>>> link2.title = "Youtube artist page"
>>> link2.url = "http://www.youtube.com/artist/lou_reed"
>>> link2.is_external = True
>>> link2.content_object = lour_reed
>>> link2.save()

>>> from generic_links.utils import get_links_for
>>> qs = get_links_for(lou_reed, is_external=True)
[<GenericLink: http://en.wikipedia.org/wiki/Lou_Reed>,
<GenericLink: http://www.youtube.com/artist/lou_reed>]

```

Generic Links admin
--------------------------------------------------------------------------------

Since a GenericLink instnace will be associated to another object you usally
wish to show an inline model admin form in that model form. 


``` python
# this is your app's admin.py
from django.contrib import admin

from generic_links.admin import GenericLinkStackedInline

from my_app.models import MyModel


class MyModelAdmin(admin.ModelAdmin):
    # ...
    inlines = [GenericLinkStackedInline]
    # ...


admin.site.register(MyModel, MyModelAdmin)
```

Using django-generic-links templatetags
--------------------------------------------------------------------------------

Now guess you have an artist page. You're passing `artist` object using template
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

Questions, Comments, etc?
--------------------------------------------------------------------------------
You may use Github comments to comment this code or the project issues to open
issues if you find a bug or a missing feature you'd like to have.

You can also follow me on Twitter - **[@matagus](http://twitter.com/matagus)**.

Want to help?
--------------------------------------------------------------------------------
If you'd like to help, write example code, contribute patches, document things
on the wiki your help is always appreciated! Just fork the project, clone your
repo, commit, push and send me a pull request

License
--------------------------------------------------------------------------------

`django-generic-links` is released under an BSD License - see the `LICENSE` file
for more information.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/matagus/django-generic-links/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

