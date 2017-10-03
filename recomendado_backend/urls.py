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

urlpatterns = router.urls

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^professional-reviews/(?P<professional>[-\w]+)/$', ProfessionalReviewList.as_view()),
    url(r'^professional-announcements/(?P<professional>[-\w]+)/$', ProfessionalAnnouncementList.as_view()),
]
