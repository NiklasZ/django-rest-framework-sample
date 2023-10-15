from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    """
    Model for a note
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField()
    # Declare owner as foreign key of user and make it so that user deletion results in deletion of that user's notes
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']  # by default, yield notes in reverse chronological order
