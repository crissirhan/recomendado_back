from rest_framework import serializers
from users.models import *


class ClientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    class Meta:
        model = Client
        fields = ("id","username","first_name", "last_name", "email")

class ProfessionalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Professional
        fields = ("id", "username", "first_name", "last_name", "email", "rut", "region", "city", "street", "house_number", "phone_number", "identification")

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id","service", "rating", "client_comment", "professional_response", "date")
        depth = 2

class AnnouncementSerializer(serializers.ModelSerializer):
    availability = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ("id","professional", "publish_date", "expire_date", "job", "location", "availability", "movility")
        depth = 1

    def get_availability(self,obj):
        return obj.get_availability_display()

class JobSubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSubCategory
        fields = ("id","job_sub_type",)
        depth = 0

class JobCategoriesSerializer(serializers.ModelSerializer):
    sub_type = JobSubCategoriesSerializer(many=True)
    class Meta:
        model = JobCategory
        fields = ("id","job_type","sub_type")
        depth = 1

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id","announcement","client")
        depth = 1
