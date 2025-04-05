from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from layout.models import Box, OperationLog

class LayoutAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.box = Box.objects.create(x=50, y=50, width=100, height=100, owner=self.user, color="#FF0000")
        OperationLog.objects.create(box=self.box, action='drag', x=50, y=50, width=100, height=100)

    def test_get_boxes(self):
        response = self.client.get('/api/boxes/')
        self.assertEqual(response.status_code, 200)
        # Assuming the serializer returns a list of boxes.
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.box.id)

    def test_get_logs(self):
        response = self.client.get('/api/logs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
