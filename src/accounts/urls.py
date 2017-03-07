from django.conf.urls import url,static
from django.conf import settings
from . import views
app_name='accounts'
urlpatterns=[
    url(r'^$',views.Indexpage.as_view(),name="index"),
    url(r'^register/$', views.Registerpage.as_view(), name="register"),
    url(r'^profile/(?P<slug>[\w-]+)/$',views.profileview,name="profile"),
    url(r'^home/',views.Homepage.as_view(),name="home"),
    url(r'^logout/',views.logoutview,name="logout"),
    url(r'^validate_username',views.validate_username,name="validateusername"),

]
