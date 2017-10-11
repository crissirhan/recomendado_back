# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from users.models import *
from users.serializers import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Count, Avg


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

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfessionalReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "professional"

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

class ProfessionalAnnouncementList(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "professional"

    def get_queryset(self):
        professional_id = self.kwargs.get(self.lookup_url_kwarg)
        announcement = Announcement.objects.filter(professional__id = professional_id)
        return announcement

class ProfessionalByUsernameList(generics.ListAPIView):
    serializer_class = ProfessionalSerializer
    lookup_url_kwarg = "username"

    def get_queryset(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        professional = Professional.objects.filter(user__username = username)
        return professional

class ClientByUsernameList(generics.ListAPIView):
    serializer_class = ClientSerializer
    lookup_url_kwarg = "username"

    def get_queryset(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        client = Client.objects.filter(user__username = username)
        return client

class AnnouncementByJobCategoryViewSet(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Announcement.objects.filter(job__id=category_id)
        return queryset

class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategoriesSerializer

class JobSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobSubCategory.objects.all()
    serializer_class = JobSubCategoriesSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer
