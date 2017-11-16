# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters
from users.models import *
from django.db.models import Avg, Count

class AnnouncementFilter(filters.FilterSet):
    min_price = filters.NumberFilter(name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(name="price", lookup_expr='lte')
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    professional = filters.CharFilter(name='professional__user__username', lookup_expr='icontains')
    professional_first_name = filters.CharFilter(name='professional__user__first_name', lookup_expr='icontains')
    professional_last_name = filters.CharFilter(name='professional__user__last_name', lookup_expr='icontains')
    job = filters.CharFilter(name='job_tags__job__job_sub_type', lookup_expr='icontains')
    tags = filters.CharFilter(method='tags_filter')
    search = filters.CharFilter(method='search_filter')
    min_publish_date = filters.IsoDateTimeFilter(name="publish_date",lookup_expr='gte')
    max_publish_date = filters.IsoDateTimeFilter(name="publish_date",lookup_expr='lte')
    min_rating = filters.NumberFilter(method='min_rating_filter')
    min_review_count = filters.NumberFilter(method='min_review_count_filter')


    class Meta:
        model = Announcement
        fields = ['id', 'title', 'description', 'max_price', 'min_price', 'job','tags', 'professional', 'professional_first_name', 'professional_last_name', 'location', 'search','min_publish_date', 'max_publish_date', 'min_rating' , 'visible']

    def search_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                title__icontains=value,
            ) | queryset.filter(
                description__icontains=value,
            ) | queryset.filter(
                professional__user__first_name__icontains=value,
            ) | queryset.filter(
                professional__user__last_name__icontains=value,
            ) | queryset.filter(
                professional__user__email__icontains=value,
            ) | queryset.filter(
                job_tags__job__job_sub_type__icontains=value,
            )
        return queryset.distinct()
    def min_rating_filter(self, queryset, name, value):
        if value:
            queryset = queryset.annotate(average_rating = Avg('service__review__rating')).filter(average_rating__gte=value)
        return queryset
    def min_review_count_filter(self, queryset, name, value):
        if value:
            queryset = queryset.annotate(review_count = Count('service__review__rating')).filter(review_count__gte=value)
        return queryset
    def tags_filter(self, queryset, name, value):
        if value:
            for val in value:
                queryset = queryset.filter(job_tags__job__id=val)
        return queryset
