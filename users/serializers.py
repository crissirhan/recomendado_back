from rest_framework import serializers
from users.models import Client, Professional, Review

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("first_name", "email")

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ("first_name", "email")

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("rating", "comment", "date")
