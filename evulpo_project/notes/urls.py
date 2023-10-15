from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from notes import views

urlpatterns = [
    path('', views.NoteList.as_view(), name='note-list-root'),  # all notes
    path('notes/', views.NoteList.as_view(), name='note-list'),

    path('notes/<int:pk>/', views.NoteDetail.as_view(), name='note-detail'),  # specific note by id
    path('users/', views.UserList.as_view(), name='user-list'),  # all users
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),  # specific user by id
    path('users/<int:user_id>/notes/', views.UserNotesList.as_view(), name='user-notes-list'),  # specific user's notes
]

# Support different formats for returned data
urlpatterns = format_suffix_patterns(urlpatterns)
