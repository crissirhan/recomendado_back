# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters
from users.models import *

class AnnouncementFilter(filters.FilterSet):
    min_price = filters.NumberFilter(name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(name="price", lookup_expr='lte')
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    professional = filters.CharFilter(name='professional__user__username', lookup_expr='icontains')
    professional_first_name = filters.CharFilter(name='professional__user__first_name', lookup_expr='icontains')
    professional_last_name = filters.CharFilter(name='professional__user__last_name', lookup_expr='icontains')
    job = filters.CharFilter(name='job_tags__job__job_sub_type', lookup_expr='icontains')

    class Meta:
        model = Announcement
        fields = ['title', 'description', 'max_price', 'min_price', 'job', 'professional', 'professional_first_name', 'professional_last_name', 'location' ]
