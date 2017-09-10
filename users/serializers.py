from rest_framework import serializers
from users.models import Client, Professional, Review, Announcement

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("first_name", "last_name", "email")

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ("first_name", "last_name", "email", "rut", "region", "city", "street", "house_number", "phone_number", "identification")

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("client", "professional", "rating", "comment", "date")

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ("professional", "publish_date", "expire_date", "job", "location", "availability", "movility")
