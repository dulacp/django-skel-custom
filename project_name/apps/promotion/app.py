from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from libs.application import Application
from apps.promotion import views


class PromotionApplication(Application):
    name = 'promotion'

    home_view = views.HomeView

    def get_urls(self):
        urlpatterns = super(PromotionApplication, self).get_urls()
        urlpatterns += patterns('',
            url(r'^$', self.home_view.as_view(), name="home"),
        )
        return self.post_process_urls(urlpatterns)

application = PromotionApplication()
