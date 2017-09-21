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
    class Meta:
        model = Announcement
        fields = ("id","professional", "publish_date", "expire_date", "job", "location", "availability", "movility")
