from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^add_quote$', views.add_quote),
    url(r'^users/(?P<id>\d+)$', views.user_profile),
    url(r'^users/favorite/(?P<id>\d+)$', views.favorite),
    url(r'^users/remove_favorite/(?P<id>\d+)$', views.remove_favorite),    
]
