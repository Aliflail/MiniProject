from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^createtestview/',views.createtestview.as_view(),name="test"),
    url(r'^ctest/(?P<ctest_id>[0-9]+)/$',views.ctest.as_view(),name="ctest"),
    url(r'^ctestexpire/',views.ctestexpire,name="ctestexpire"),
    url(r'^cupdatetime/',views.cupdatetime,name="cupdatetime"),
]