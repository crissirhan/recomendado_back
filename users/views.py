# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from users.models import Client, Professional, Review, Announcement
from users.serializers import ClientSerializer, ProfessionalSerializer, ReviewSerializer, AnnouncementSerializer, JobCategoriesSerializer
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

class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class ListJobCategories(APIView):
    def get(self, request):
        return Response(Announcement.JOB_CATEGORIES)

class ProfessionalReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "professional"

    def get_queryset(self):
        professional_id = self.kwargs.get(self.lookup_url_kwarg)
        professional = Professional.objects.filter(id=professional_id)
        reviews = Review.objects.filter(professional= professional)
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
