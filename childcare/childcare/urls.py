"""childcare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from track.views import IndexView, Start_View, UserCreateView, ChildCreateView, CheckinCreateView,\
                        StaffListView, CheckinUpdateView, ProfileListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name="index_view"),
    url(r'^start/$', Start_View.as_view(), name="start_view"),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^create_child/$', ChildCreateView.as_view(), name="child_create_view"),
    url(r'^staff/$', StaffListView.as_view(), name="staff_list_view"),
    url(r'^/accounts/profile/$', ProfileListView.as_view(), name="profile_list_view"),
    url(r'^checkin/(?P<pk>\d+)/$', CheckinCreateView.as_view(), name="checkin_create_view"),
    url(r'^checkin_update/(?P<pk>\d+)/$', CheckinUpdateView.as_view(), name="checkin_update_view")
]
