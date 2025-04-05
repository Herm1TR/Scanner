from django.test import TestCase
from django.contrib.auth import get_user_model
from layout.models import Box, OperationLog

class BoxModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_box_str(self):
        box = Box.objects.create(x=10, y=20, width=150, height=150, owner=self.user, color="#00FF00")
        expected_str = f"Box({box.id}) owned by {self.user} - x:{box.x}, y:{box.y}, w:{box.width}, h:{box.height}"
        self.assertEqual(str(box), expected_str)

class OperationLogModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.box = Box.objects.create(x=10, y=20, width=150, height=150, owner=self.user, color="#00FF00")

    def test_operation_log_str(self):
        log = OperationLog.objects.create(box=self.box, action='drag', x=10, y=20, width=150, height=150)
        # Verify that the string representation contains key elements.
        self.assertIn(f"Box {self.box.id}", str(log))
        self.assertIn("drag", str(log))
