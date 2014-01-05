# encoding: utf-8

from django.views import generic
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
    

class HomeView(generic.TemplateView):
    template_name = "promotion/home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        return ctx
