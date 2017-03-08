from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'(?P<test_id>[0-9]+)/$',views.testpage.as_view(),name="test"),
    url(r'(?P<test_id>[0-9]+)/result/$',views.resultpage.as_view(),name="result"),
    url(r'^createtest/', views.createtest.as_view(), name="createtest"),
    url(r'^createquestion/$',views.createquestion.as_view(),name="createquestion"),
    url(r'^createanswer/$',views.createanswer.as_view(),name="createanswer"),
    url(r'^testexpire/',views.testexpire,name="testexpire"),
    url(r'^updatetime/',views.updatetime,name="updatetime"),
]
