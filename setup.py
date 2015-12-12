# -*- coding: UTF-8 -*-
from setuptools import setup
from generic_links import get_version


setup(
    name='django-generic-links',
    version=get_version(),
    license='BSD License Version 2',
    description='Simple and generic application for Django projects to attach and handle links for any object',
    long_description=('It provides a model, admin model and templatetags to attach links to any model instance and retrive and handle them.'),
    keywords='django apps links generic',
    author='Matías Agustín Méndez',
    author_email='matagus@gmail.com',
    url='http://matagus.github.com/django-generic-links/',
    packages=['generic_links', 'generic_links.templatetags', 'generic_links.migrations', ],
    tests_require=['django>=1.8,<1.10', ],
    test_suite='runtests.runtests',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
