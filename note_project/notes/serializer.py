from django.contrib.auth.models import User
from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        # Use only user id for serialization
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['owner', 'id', 'title', 'body']


class UserSerializer(serializers.ModelSerializer):
    # Get user's note ids
    notes = serializers.PrimaryKeyRelatedField(many=True, queryset=Note.objects.all())

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'notes']
