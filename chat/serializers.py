from rest_framework import serializers
from chat.models import Thread
from user.serializers import UserThreadListSerializer


class ThreadCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ["id", "participants", "created", "updated"]

    def validate(self, attrs):
        creator = self.context["request"].user
        participants = attrs.get("participants", [])
        if len(participants) == 0:
            raise serializers.ValidationError("You need to have correspondent")
        if len(participants) > 1:
            raise serializers.ValidationError("Thread can not have more then two participants")
        if creator in participants:
            raise serializers.ValidationError("You can not add your self to thread")
        data = super(ThreadCreateSerializer, self).validate(attrs)
        return data

    def create(self, validated_data):
        participants = validated_data.pop("participants")
        creator = self.context["request"].user
        old_thread = Thread.objects.filter(participants=creator).filter(participants=participants[0])
        if len(old_thread) != 0:
            return old_thread[0]
        thread = Thread.objects.create(**validated_data)
        thread.participants.set(participants)
        thread.participants.add(creator)

        return thread


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserThreadListSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ["id", "participants", "created", "updated"]
