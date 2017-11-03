# -*- coding: utf-8 -*-
"""recomendado_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from users.views import *

router = DefaultRouter()
router.register(prefix='clients', viewset=ClientViewSet)
router.register(prefix='professionals', viewset=ProfessionalViewSet)
router.register(prefix='reviews', viewset=ReviewViewSet)
router.register(prefix='announcements', viewset=AnnouncementViewSet)
router.register(prefix='job-categories', viewset=JobCategoryViewSet)
router.register(prefix='job-sub-categories', viewset=JobSubCategoryViewSet)
router.register(prefix='services', viewset=ServiceViewSet)
router.register(prefix='job-tags', viewset=JobTagViewSet)
router.register(prefix='announcement-images', viewset=AnnouncementImageViewSet)
router.register(base_name="post",prefix='post-services', viewset=PostServiceViewSet)
router.register(base_name="post",prefix='post-reviews', viewset=PostReviewViewSet)
router.register(base_name="post",prefix='post-announcements', viewset=PostAnnouncementViewSet)
urlpatterns = router.urls

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^professional-reviews/(?P<professional>[-\w]+)/$', ProfessionalReviewList.as_view()),
    url(r'^professional-announcements/(?P<professional>[-\w]+)/$', ProfessionalAnnouncementList.as_view()),
    url(r'^client-services/(?P<client>[-\w]+)/$', ClientServiceList.as_view()),
    url(r'^announcements/job/(?P<category_name>[-\w]+)/$', AnnouncementByJobCategoryViewSet.as_view()),
    url(r'^job-sub-categories/name/(?P<name>[-\w]+)/$', JobsByNameViewSet.as_view()),
    url(r'^announcements/job-subtype/(?P<sub_category_name>[-\w]+)/$', AnnouncementByJobSubCategoryViewSet.as_view()),
    url(r'^professionals-username/(?P<username>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', ProfessionalByUsernameList.as_view()),
    url(r'^clients-username/(?P<username>.+)/$', ClientByUsernameList.as_view()),
    url(r'^client-reviews/(?P<client>[-\w]+)/$', ClientReviewsList.as_view()),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
]
