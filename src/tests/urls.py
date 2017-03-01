from django.conf.urls import url,include
from . import views
urlpatterns = [

    url(r'(?P<test_id>[0-9]+)/$',views.testpage.as_view(),name="test"),
    url(r'(?P<test_id>[0-9]+)/result/$',views.resultpage.as_view(),name="result"),

]
