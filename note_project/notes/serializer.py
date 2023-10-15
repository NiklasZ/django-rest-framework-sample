from django.contrib.auth.models import User
from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        # Use only user id for serialization
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['owner', 'id', 'title', 'body', 'created']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']
