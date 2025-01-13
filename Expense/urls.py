"""
URL configuration for Expense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from ExpenseMate import views
from ExpenseMate.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('delete/<int:id>/',delete_rec),
    path('',login_page),
    path('logout/',logout_user),
    path('dashboard/',dashboard),
    path('history/',history_view),
    path('about_page/',aboutpage),
    path('dashboard/add/',add_expense),
    path('dashboard/add/<id>',add_expense),
    path('dashboard/budget/',setbudget),
    path('register/',register),
]

if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

urlpatterns+=staticfiles_urlpatterns()