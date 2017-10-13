from rest_framework import serializers, fields
from users.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['password']
        read_only_fields = ['id']
        fields = ("id","username","password","first_name", "last_name", "email")

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Client
        fields = ("id", "user")
        depth = 2

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        client = Client.objects.create(user=user, **validated_data)
        print(client)
        print(user)
        return client

class ProfessionalSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Professional
        fields = ("id", "user", "rut", "region", "city", "street", "house_number", "phone_number", "identification")
        depth = 2

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        professional = Professional.objects.create(user=user, **validated_data)
        return professional


class AnnouncementSerializer(serializers.ModelSerializer):
    availability_display = serializers.SerializerMethodField()
    availability = fields.MultipleChoiceField(choices=Announcement.WEEKDAYS)
    #weekdays = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ("id","professional", "publish_date", "expire_date", "job", "location", "availability","availability_display","movility")
        depth = 2

    def get_availability_display(self,obj):
        return obj.get_availability_display()

    def get_weekdays(self,obj):
        return obj.get_weekdays()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class JobSubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSubCategory
        fields = ("id","job_sub_type",)
        depth = 2

class JobCategoriesSerializer(serializers.ModelSerializer):
    sub_type = JobSubCategoriesSerializer(many=True)
    class Meta:
        model = JobCategory
        fields = ("id","job_type","sub_type")
        depth = 2

class ServicesSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    announcement = AnnouncementSerializer(many=False)
    class Meta:
        model = Service
        fields = ("id","announcement","client")

class PostServicesSerializer(serializers.ModelSerializer):
    client_id= serializers.PrimaryKeyRelatedField(source='client',read_only=False, queryset=Client.objects.all())
    announcement_id = serializers.PrimaryKeyRelatedField(source='announcement',read_only=False, queryset=Announcement.objects.all())
    class Meta:
        model = Service
        fields = ("id","announcement_id","client_id")
    def create(self, validated_data):
        print(validated_data)
        client_data = validated_data.pop('client')
        client = Client.objects.get(id=client_data.id)
        print(client_data.id)
        announcement_data = validated_data.pop('announcement')
        announcement = Announcement.objects.get(id=announcement_data.id)
        service = Service.objects.create(client=client, announcement=announcement, **validated_data)
        return service
class PostReviewsSerializer(serializers.ModelSerializer):
    service_id= serializers.PrimaryKeyRelatedField(source='service',read_only=False, queryset=Service.objects.all())
    class Meta:
        model = Review
        fields = ("id","service_id","date","client_comment","rating")
    def create(self, validated_data):
        print(validated_data)
        service_data = validated_data.pop('service')
        service = Service.objects.get(id=service_data.id)
        review = Review.objects.create(service=service, **validated_data)
        return review

class ReviewSerializer(serializers.ModelSerializer):
    service = ServicesSerializer(many=False)
    class Meta:
        model = Review
        fields = ("id","service", "rating", "client_comment", "professional_response", "date")
        depth = 5
    def create(self, validated_data):
        service_data = validated_data.pop('service')
        service = Service.objects.filter(id=service_data.id)
        review = Review.objects.create(service=service, **validated_data)
        return review
