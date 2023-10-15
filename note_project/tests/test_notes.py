from unittest import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from notes.models import Note


class NoteTests(TestCase):
    def setUp(self):
        Note.objects.all().delete()
        User.objects.all().delete()

        self.client = APIClient()
        self.user = User.objects.create_user(username='joe', password='pass')
        self.client.login(username='joe', password='pass')
        self.other_user = User.objects.create_user(username='sara', password='pass')
        self.client.login(username='sara', password='pass')

        self.note_data = {'title': 'Cookie recipe', 'body': 'sugar, eggs, flour, chocolate', 'owner': self.user.id}
        self.response = self.client.post(
            reverse('note-list'),
            self.note_data,
            format='json'
        )

        self.note_data = {'title': 'Soup recipe', 'body': 'water, vegetable stock, carrots, onions',
                          'owner': self.other_user.id}
        self.other_response = self.client.post(
            reverse('note-list'),
            self.note_data,
            format='json'
        )

    def tearDown(self):
        self.client.logout()
        Note.objects.all().delete()
        User.objects.all().delete()

    def test_create_note(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        self.assertEqual(Note.objects.get(title='Cookie recipe').title, 'Cookie recipe')

    def test_read_note(self):
        note = Note.objects.get(title='Cookie recipe')
        response = self.client.get(reverse('note-detail', args=[note.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], note.title)

    def test_read_notes_by_user(self):
        note = Note.objects.get(title='Cookie recipe')
        response = self.client.get(reverse('user-notes-list', args=[note.owner.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], note.title)

    def test_update_note(self):
        note = Note.objects.get(title='Cookie recipe')
        updated_data = {'title': 'Updated Title', 'body': 'Updated body.', 'owner': self.user.id}
        response = self.client.put(reverse('note-detail', args=[note.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(note.title, 'Updated Title')

    def test_delete_note(self):
        note = Note.objects.get(title='Cookie recipe')
        response = self.client.delete(reverse('note-detail', args=[note.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 1)

    def test_delete_user_cascades_note(self):
        note = Note.objects.get(title='Soup recipe')
        response = self.client.delete(reverse('user-detail', args=[note.owner.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
