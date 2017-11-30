# -*- coding: utf-8 -*-
from rest_framework import serializers, fields
from users.models import *
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['password']
        read_only_fields = ['id']
        fields = ("id","username","password","first_name", "last_name", "email")

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    profile_picture = Base64ImageField(required=False)
    class Meta:
        model = Client
        fields = ("id", "user", "profile_picture")
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
        user, created = User.objects.get_or_create(**user_data)
        user.set_password(password)
        user.save()
        client = Client.objects.create(user=user, **validated_data)
        return client

class ProfessionalSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    profile_picture = Base64ImageField(required=False)
    class Meta:
        model = Professional
        fields = ("id", "average", "count", "user","experience", "rut", "region", "city", "street", "house_number", "phone_number", "identification", "profile_picture")
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
        user, created = User.objects.get_or_create(**user_data)
        user.set_password(password)
        user.save()
        professional = Professional.objects.create(user=user, **validated_data)
        return professional

class CompleteUserSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    professional = ProfessionalSerializer(many=False)
    class Meta:
        model = User
        write_only_fields = ['password']
        read_only_fields = ['id']
        fields = ("id","username","password","first_name", "last_name", "email", "client", "professional")
        depth = 2

class AnnouncementImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    class Meta:
        model= AnnouncementImage
        fields= ("id", "image", "announcement")
        depth = 2

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class JobSubCategoriesSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=JobSubCategory()._meta.get_field('id'))
    image = Base64ImageField(required=False)
    class Meta:
        model = JobSubCategory
        fields = ("id","job_sub_type","job_category", "description", "image")
        depth = 2

class JobSubCategoriesAuxSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=JobSubCategory()._meta.get_field('id'))
    class Meta:
        model = JobSubCategory
        fields = ("id", "job_sub_type", "job_category", "description")
        depth = 2

class JobTagSerializer(serializers.ModelSerializer):
    #job_id = serializers.PrimaryKeyRelatedField(source='job',read_only=False, queryset=JobCategory.objects.all())
    job = JobSubCategoriesAuxSerializer(many=False)
    class Meta:
        model = JobTag
        fields = ("id", "announcement", "job")
        depth = 3
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
            "job": {
                "read_only": False,
            }
        }
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    def create(self, validated_data):
        job_data = validated_data.pop('job')
        job = JobSubCategory.objects.get(id=job_data.id)
        job_tag, created = JobTag.objects.get_or_create(job=job, **validated_data)
        return job_tag

class AnnouncementSerializer(serializers.ModelSerializer):
    availability_display = serializers.SerializerMethodField()
    availability = fields.MultipleChoiceField(choices=Announcement.WEEKDAYS)
    announcement_thumbnail = Base64ImageField(required=False)
    job_tags = JobTagSerializer(many=True)
    announcement_images = AnnouncementImageSerializer(many=True)
    professional_id= serializers.PrimaryKeyRelatedField(source='professional',read_only=False, queryset=Professional.objects.all())
    review_count = serializers.FloatField(read_only = True)
    review_average = serializers.FloatField(read_only = True)

    class Meta:
        model = Announcement
        fields = ("id", "review_count", "review_average", "visible", "title", "description", "announcement_images", "job_tags", "professional", "professional_id", "price", "publish_date", "expire_date", "location", "approved", "availability","availability_display","movility", "announcement_thumbnail")
        depth = 3

    def get_availability_display(self,obj):
        return obj.get_availability_display()

    def get_weekdays(self,obj):
        return obj.get_weekdays()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        images_data = validated_data.pop('announcement_images')
        job_tags_data = validated_data.pop('job_tags')
        professional_data = validated_data.pop('professional')
        professional = Professional.objects.get(id=professional_data.id)
        announcement, created = Announcement.objects.get_or_create(professional=professional, **validated_data)
        for image_data in images_data:
            image, created = AnnouncementImage.objects.get_or_create(announcement=announcement, **image_data)
        for job_tag_data in job_tags_data:
            job_data = job_tag_data.pop('job')
            job = JobSubCategory.objects.get(id=job_data["id"])
            job_tag, created = JobTag.objects.get_or_create(job=job, announcement=announcement, **job_tag_data)
        return announcement


class JobCategoriesSerializer(serializers.ModelSerializer):
    sub_type = JobSubCategoriesSerializer(many=True)
    class Meta:
        model = JobCategory
        fields = ("id","job_type","sub_type", "description", "image")
        depth = 2

class ServicesSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    announcement = AnnouncementSerializer(many=False)
    class Meta:
        model = Service
        fields = ("id","announcement","client", "cost" , "creation_date")

class PostServicesSerializer(serializers.ModelSerializer):
    client_id= serializers.PrimaryKeyRelatedField(source='client',read_only=False, queryset=Client.objects.all())
    announcement_id = serializers.PrimaryKeyRelatedField(source='announcement',read_only=False, queryset=Announcement.objects.all())
    class Meta:
        model = Service
        fields = ("id","announcement_id","client_id", "cost" , "creation_date")
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

class PostAnnoucementSerializer(serializers.ModelSerializer):
    professional_id= serializers.PrimaryKeyRelatedField(source='professional',read_only=False, queryset=Professional.objects.all())
    job_id = serializers.PrimaryKeyRelatedField(source='job',read_only=False, queryset=JobCategory.objects.all())
    availability = fields.MultipleChoiceField(choices=Announcement.WEEKDAYS)
    announcement_thumbnail = Base64ImageField(required=False)
    class Meta:
        model = Announcement
        fields = ("id","title", "visible", "description", "price", "professional_id","job_id","job_subtype_id", "publish_date", "expire_date", "location", "availability", "movility", "announcement_thumbnail")
    def create(self, validated_data):
        print(validated_data)
        professional_data = validated_data.pop('professional')
        professional = Professional.objects.get(id=professional_data.id)
        job_data = validated_data.pop('job')
        job = JobCategory.objects.get(id=job_data.id)
        if 'job_subtype' in validated_data:
            job_subtype_data = validated_data.pop('job_subtype')
            if job_subtype_data.id:
                job_subtype = JobSubCategory.objects.get(id=job_subtype_data.id)
                announcement = Announcement.objects.create(professional=professional, job=job, job_subtype=job_subtype, **validated_data)
                return announcement
        announcement = Announcement.objects.create(professional=professional, job=job, **validated_data)
        return announcement

class ReviewSerializer(serializers.ModelSerializer):
    service = ServicesSerializer(many=False)
    review_count = serializers.FloatField(read_only = True)
    review_average = serializers.FloatField(read_only = True)
    class Meta:
        model = Review
        fields = ("id","service","review_count", "review_average", "rating", "client_comment", "professional_response", "date")
        depth = 5
    def create(self, validated_data):
        service_data = validated_data.pop('service')
        service = Service.objects.filter(id=service_data.id)
        review = Review.objects.create(service=service, **validated_data)
        return review
