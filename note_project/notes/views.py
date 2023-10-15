from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from notes.models import Note
from notes.serializer import NoteSerializer, UserSerializer


# We're using API Views here. These are less expressive than functional views, but also much shorter.

class NoteList(generics.ListCreateAPIView):
    """
    GET list of notes or POST a new note
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET a specific note, PUT a new note (update), or DELETE a note
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class UserList(generics.ListCreateAPIView):
    """
    GET list of users or POST a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveDestroyAPIView):
    """
    GET a specific user or DELETE a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserNotesList(generics.ListAPIView):
    """
    GET a list of notes for a specific user
    """
    serializer_class = NoteSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(get_user_model(), pk=user_id)
        return Note.objects.filter(owner=user.id)
