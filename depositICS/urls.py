"""depositICS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import views as auth_views
from core.views import SwotListView, SwotUpdateView, SwotCreateView, SwotDeleteView, AnalysisListView, ReportListView, \
    ReportCreateView, ReportDeleteView, ReportUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^adminactions/', include('adminactions.urls')),
    url(r'^report_builder/', include('report_builder.urls')),
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'},
        name='auth_logout'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),
        name='registration_complete'),
    url(r'^swot/$', SwotListView.as_view(), name='swot'),
    url(r'^swot/(?P<pk>\d+)/edit/$', SwotUpdateView.as_view(), name='swot_edit'),
    url(r'^swot/add/$', SwotCreateView.as_view(), name='swot_add'),
    url(r'^swot/(?P<pk>\d+)/del/$', SwotDeleteView.as_view(), name='swot_del'),
    url(r'^analysis/$', AnalysisListView.as_view(), name="analysis"),
    url(r'^reports/$', ReportListView.as_view(), name='report'),
    url(r'^reports/add/$$', ReportCreateView.as_view(), name='report_add'),
    url(r'^reports/(?P<pk>\d+)/edit/$', ReportUpdateView.as_view(), name='report_edit'),
    url(r'^reports/(?P<pk>\d+)/del/$', ReportDeleteView.as_view(), name='report_del'),
]
