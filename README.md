# Django Skel optimized for Heroku


## Requirements

You need to install some pretty useful thing to be able to run this project, here is the list

* Homebrew : first of all, to helps you in managing the following dependencies.

Then :

* LibJPEG : `$ brew install libjpeg`
    > you'll probably needs this if you want to make some thumbnails of jpeg images.

* `virtualenv` and `virtualenvwrapper`
* Redis : `$ brew install redis`
* PostgreSQL : `$ brew install postgresql`
* RabbitMQ : `$ brew install rabbitmq`


## Installation

```sh
$ mkvirtualenv myproject
$ workon myproject
$ pip install 'Django<1.7'
$ django-admin.py startproject --template=https://github.com/dulaccc/django-skel-custom/zipball/master --name=Makefile myproject
$ cd myproject
$ pip install -r reqs/dev.txt
```

And you're ready to run the server :) `$ python manage.py runserver` or `$ make rs` thanks to some shortcuts defined in the `Makefile`

## Prod settings

```sh
$ heroku config:add DJANGO_SETTINGS_MODULE=myproject.settings.prod
```


## Contact

[Pierre Dulac](http://github.com/dulaccc)  
[@dulaccc](https://twitter.com/dulaccc)
