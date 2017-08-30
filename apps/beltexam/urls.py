from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),    # This line has changed!
    url(r'^create$', views.create),
    url(r'^login$', views.login), 
    url(r'^success$', views.success), 
    url(r'^addproduct$', views.addproduct), 
    url(r'^addcreate$', views.addcreate), 
    url(r'^join/(?P<id>\d+)$', views.join_wish_items), 
    url(r'^wish_items/(?P<id>\d+)$', views.wishlist), 
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^remove/(?P<id>\d+)$', views.remove),

]