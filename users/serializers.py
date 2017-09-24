from rest_framework import serializers
from users.models import Client, Professional, Review, Announcement

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id","first_name", "last_name", "email")

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ("id","first_name", "last_name", "email", "rut", "region", "city", "street", "house_number", "phone_number", "identification")

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id","client", "professional", "rating", "comment", "date")

class AnnouncementSerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ("id","professional", "publish_date", "expire_date", "job", "location", "availability", "movility")

    def get_job(self,obj):
        return obj.get_job_display()

    def get_availability(self,obj):
        return obj.get_availability_display()

class JobCategoriesSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Announcement

    def get_categories(self,obj):
        return obj.JOB_CATEGORIES
