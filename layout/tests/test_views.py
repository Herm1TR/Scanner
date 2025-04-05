import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from layout.models import Box

class LayoutViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.floorplan_url = reverse('floorplan')
        self.update_box_url = reverse('update_box')
        self.user_credentials = {
            'username': 'testuser',
            'password1': 'password12345',
            'password2': 'password12345'
        }

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_post(self):
        response = self.client.post(self.register_url, data=self.user_credentials)
        # Expect redirect after successful registration.
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(username='testuser')
        # A default box should have been created for the new user.
        self.assertTrue(Box.objects.filter(owner=user).exists())

    def test_floorplan_view_requires_login(self):
        response = self.client.get(self.floorplan_url)
        # Should redirect to login if not authenticated.
        self.assertNotEqual(response.status_code, 200)

    def test_floorplan_view_authenticated(self):
        user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.floorplan_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'layout/floorplan.html')

    def test_update_box_view(self):
        user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        # Create a box to be updated.
        box = Box.objects.create(x=50, y=50, width=100, height=100, owner=user, color="#FF0000")
        data = {
            'id': box.id,
            'x': 60,
            'y': 60,
            'width': 110,
            'height': 110,
            'action': 'update'
        }
        response = self.client.post(self.update_box_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        box.refresh_from_db()
        self.assertEqual(box.x, 60)
        self.assertEqual(box.y, 60)
