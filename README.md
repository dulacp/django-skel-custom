# Django Skel optimized for Heroku

## Installation

```sh
$ mkvirtualenv myproject
$ workon myproject
$ pip install 'Django<1.7'
$ django-admin.py startproject --template=https://github.com/dulaccc/django-skel-custom/zipball/master --name=Makefile myproject
$ heroku config:add DJANGO_SETTINGS_MODULE=myproject.settings.prod
```

## Contact

[Pierre Dulac](http://github.com/dulaccc)  
[@dulaccc](https://twitter.com/dulaccc)
