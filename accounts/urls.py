from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$',views.Indexpage.as_view(),name="index"),
    url(r'^register/$', views.Registerpage.as_view(), name="register"),
    url(r'^home/',views.Homepage.as_view(),name="home"),
]