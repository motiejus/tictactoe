from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='contest/index.html'),
        name='index'),
    url(r'rules$', TemplateView.as_view(template_name='contest/rules.html'),
        name='rules'),

    url(r'^caps_left$', 'tictactoe.contest.views.caps_left'),
    url(r'^upload$', 'tictactoe.contest.views.upload'),
    url(r'^ranking$', 'tictactoe.contest.views.ranking'),
    url(r'^entries$', 'tictactoe.contest.views.entries'),
    url(r'^entries/(?P<uid>\d+)$', 'tictactoe.contest.views.entries'),
    url(r'^entry/(?P<id>\d+)$', 'tictactoe.contest.views.entry'),
    url(r'^fight/(?P<id>\d+)$', 'tictactoe.contest.views.fight'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),

)
