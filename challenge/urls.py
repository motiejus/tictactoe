from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='contest/index.html')),

    url(r'^upload/$', 'challenge.contest.views.upload'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login',
        {'extra_context': {'next': '/'}}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
)
