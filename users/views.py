        # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from users.models import *
from users.serializers import *
from users.filters import *
from users.pagination import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Count, Avg
#from rest_framework import filters
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfessionalWithTokenViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    def list(self, request):
        queryset = Professional.objects.get(user=request.user)
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = ReviewFilter
    ordering_fields = ('date', 'rating')
    ordering = ('-date',)
    pagination_class = StandardResultsSetPagination

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(approved=True).annotate(review_count = Count('service__review')).annotate(review_average = Avg('service__review__rating'))
    serializer_class = AnnouncementSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = AnnouncementFilter
    ordering_fields = ('price', 'publish_date')
    ordering = ('-publish_date',)
    pagination_class = StandardResultsSetPagination

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AnnouncementImageViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementImage.objects.filter()
    serializer_class = AnnouncementImageSerializer

class JobTagViewSet(viewsets.ModelViewSet):
    queryset = JobTag.objects.all()
    serializer_class = JobTagSerializer

class ProfessionalReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "professional"
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = ReviewFilter
    ordering_fields = ('date', 'rating')
    ordering = ('-date',)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        professional_id = self.kwargs.get(self.lookup_url_kwarg)
        professional = Professional.objects.filter(id=professional_id)
        reviews = Review.objects.filter(service__announcement__professional__id= professional_id)
        return reviews

    def list(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ReviewSerializer(queryset, many=True)
        count = queryset.count()
        average =  queryset.aggregate(Avg('rating')).values()[0]
        data = {'reviews': serializer.data}
        data.update({
            'count':count,
            'average':average
        })
        return Response(data)

class AnnouncementReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "announcement"
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = ReviewFilter
    ordering_fields = ('date', 'rating')
    ordering = ('-date',)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        announcement_id = self.kwargs.get(self.lookup_url_kwarg)
        reviews = Review.objects.filter(service__announcement__id= announcement_id)
        return reviews

    def list(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ReviewSerializer(queryset, many=True)
        count = queryset.count()
        average =  queryset.aggregate(Avg('rating')).values()[0]
        data = {'reviews': serializer.data}
        data.update({
            'count':count,
            'average':average
        })
        return Response(data)

class ProfessionalAnnouncementList(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "professional"

    def get_queryset(self):
        professional_id = self.kwargs.get(self.lookup_url_kwarg)
        announcement = Announcement.objects.filter(professional__id = professional_id, approved=True)
        return announcement

class ClientServiceList(generics.ListAPIView):
    serializer_class = ServicesSerializer
    lookup_url_kwarg = "client"
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = ServiceFilter
    ordering_fields = ('creation_date',)
    ordering = ('-creation_date',)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        client_id = self.kwargs.get(self.lookup_url_kwarg)
        service = Service.objects.filter(client__id = client_id)
        return service

class ProfessionalByUsernameList(generics.ListAPIView):
    serializer_class = ProfessionalSerializer
    lookup_url_kwarg = "username"

    def get_queryset(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        professional = Professional.objects.filter(user__username = username)
        return professional

class ClientReviewsList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "client"
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = ReviewFilter
    ordering_fields = ('date', 'rating')
    ordering = ('-date',)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        client_id = self.kwargs.get(self.lookup_url_kwarg)
        reviews = Review.objects.filter(service__client__id = client_id)
        return reviews

class ClientByUsernameList(generics.ListAPIView):
    serializer_class = ClientSerializer
    lookup_url_kwarg = "username"

    def get_queryset(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        client = Client.objects.filter(user__username = username)
        return client

class AnnouncementByJobCategoryViewSet(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "category_name"
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AnnouncementFilter
    #filter_fields = ( 'title', 'description', 'job_tags__job__job_type', 'job_tags__job_subtype__job_sub_type', 'location', 'professional__user__email', 'professional__user__first_name', 'professional__user__last_name',)

    def get_queryset(self):
        category_name = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Announcement.objects.filter(job_tags__job__job_sub_type=category_name, approved=True)
        return queryset

class AnnouncementByJobSubCategoryViewSet(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "sub_category_name"
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AnnouncementFilter
    #filter_fields = ( 'title', 'description', 'job__job_type', 'job_subtype__job_sub_type', 'location', 'professional__user__email', 'professional__user__first_name', 'professional__user__last_name',)

    def get_queryset(self):
        category_name = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Announcement.objects.filter(job_tags__job__job_sub_type=category_name, approved=True)
        return queryset

class JobsByNameViewSet(generics.ListAPIView):
    serializer_class = JobSubCategoriesSerializer
    lookup_url_kwarg = "name"
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwarg)
        try:
            queryset = JobSubCategory.objects.filter(job_sub_type=name)
        except JobSubCategory.DoesNotExist:
            queryset = None
        return queryset

class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategoriesSerializer

class JobSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobSubCategory.objects.all()
    serializer_class = JobSubCategoriesSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.annotate(review_average = Avg('review__rating')).annotate(review_count = Count('review')).filter(deleted=False)
    serializer_class = ServicesSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = ServiceFilter
    ordering_fields = ('creation_date',)
    ordering = ('-creation_date',)
    pagination_class = StandardResultsSetPagination

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PostServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = PostServicesSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = ServiceFilter
    ordering_fields = ('creation_date',)
    ordering = ('-creation_date',)
    pagination_class = StandardResultsSetPagination

class PostReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = PostReviewsSerializer

class PostAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

# Socal login

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
