from django.test import TestCase
from datetime import datetime,timedelta
from django.utils import timezone
# from django.contrib.auth import get_user_model

from ..models import Task
from accounts.models import User, Profile


class TaskModelTest(TestCase):
    
    def setUp(self):
        # self.user = get_user_model().objects.create_user(        
        self.user = User.objects.create_user(
            id=3000,
            email='test@test.com',
            password='Test@pass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            description='Test Description'
            )
    
    def test_task_creation(self):            
        task = Task.objects.create(
            creator = self.profile,
            title='test',
            due_date = timezone.make_aware(datetime.now()) + timedelta(days=7),
            )
        self.assertEqual(task.title, 'test')
        # self.assertEqual(str(task), 'test')        
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
    