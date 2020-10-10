from rest_framework import serializers
from .models import Echo, Pledge


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.ReadOnlyField(source='supporter.username')
    project_id = serializers.PrimaryKeyRelatedField(source='project.id',queryset=Echo.objects.all())
    #project_id = serializers.IntegerField()

    def create(self,validated_data):
        pledge = Pledge.objects.create(
            project_id=validated_data['project']['id'].id,
            amount=validated_data.get('amount'),
            comment=validated_data.get('comment'),
            anonymous = validated_data.get('anonymous'),
            supporter = validated_data.get('supporter'))
        return pledge

class EchoSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length = 200)
    description = serializers.CharField(max_length=200)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.username')
    pledges = PledgeSerializer(many=True,read_only=True) #
    category = serializers.CharField(max_length=200)

    def create(self,validated_data):
        return Echo.objects.create(**validated_data)

class EchoDetailSerializer(EchoSerializer):
    pledges=PledgeSerializer(many=True,read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance



