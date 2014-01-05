from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from libs.application import Application
from apps.promotion.app import application as promotion_app


class MainApplication(Application):
    name = None

    promotion_app = promotion_app

    def get_urls(self):
        urlpatterns = patterns('',
            (r'^', include(self.promotion_app.urls)),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        pass

application = MainApplication()
