from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login$', views.user_login),
    url(r'^create$', views.create_user),
    url(r'^login/user$', views.login),
    url(r'^add/book$', views.add_book),
    url(r'^addbookdb$', views.add_book_db),
]