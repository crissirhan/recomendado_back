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
