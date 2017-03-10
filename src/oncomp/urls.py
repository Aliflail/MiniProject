from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^createtestview/',views.createtestview.as_view(),name="test")
]