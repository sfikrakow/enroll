"""workshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from mozilla_django_oidc.urls import OIDCAuthenticateClass

urlpatterns = [
    path('admin/login/', OIDCAuthenticateClass.as_view()),
    path('admin/', admin.site.urls),
    path('oidc/', include('sfi_base.urls')),
    path('', include('workshop.urls', namespace='workshop')),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
admin.site.site_title = _('Workshop administration')
admin.site.site_header = _('Workshop administration')
admin.site.index_title = _('Workshop administration')
