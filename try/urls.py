"""try URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import re_path as url
from . import search,upload,view,modify,delete,run,signup,signin,profile,data

urlpatterns = [
    path('modelplex/',view.homepage),
    path('modelplex/faq',view.faq),
    path('modelplex/search',search.search),
    path('modelplex/search_result/',search.result),
    path('modelplex/upload_model',upload.upload),
    path('modelplex/upload_model/upload_result/',upload.result),
    path('modelplex/model/<int:id>/modify_model/',modify.modify),
    path('modelplex/model/<int:id>/modify_model/modify_result/',modify.result),
    path('modelplex/model/',view.show_model),
    path('modelplex/model/<int:id>/delete_result/',delete.result),
    path('modelplex/model/<int:id>/test_model/',run.test_model),
    path('modelplex/model/<int:id>/test_model/test_result/',run.result),
    path('modelplex/signup/',signup.signup),
    path('modelplex/signin/',signin.signin),
    path('modelplex/logout/',signin.logout),
    path('modelplex/profile/',profile.profile),
    path('modelplex/modify_password/', profile.mp_view),
    path('modelplex/modi_password_result/', profile.modify_password),
    url(r'^modelplex/profile/([\w\-]+)/$', profile.profile),
    url(r'^modelplex/dataset/(\d)/$', data.dataset),
    path('modelplex/model/<int:mid>/dataset_upload/', data.dataset_upload),

]
