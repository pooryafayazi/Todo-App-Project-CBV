from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime,timedelta
from django.utils import timezone

from accounts.models import User, Profile
from tasks.models import Task


class TestTaskView(TestCase):
    
    def setUp(self):
        self.client = Client()        
        self.user = User.objects.create_user(id=300,email='t@test.com',password='T@pass123')        
        self.client.login(email='t@test.com',password='T@pass123')
        
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            description='Test Description'
            )
        self.task = Task.objects.create(
            creator = self.profile,
            title='test',
            due_date = timezone.make_aware(datetime.now()) + timedelta(days=7),
            )
    
    def test_tasks_list_url_seccessful_response(self):
        url = reverse('tasks:list_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list3.html')
        self.assertTrue(str(response.content).find('task') > 0)
        self.assertTrue(b'task' in response.content)     
        
        
    def test_task_detail_logged_in_user(self):
        pass
    
        
    def test_task_detail_logged_out_user(self):
        # self.client.logout()
        url = reverse('tasks:task-update', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, f'/accounts/login/?next={url}')
        
        
        
class TestTaskView(TestCase):
    
    def setUp(self):
        self.client = Client()        
        self.user = User.objects.create_user(id=300,email='t@test.com',password='T@pass123')        
        
        # Ensure only one profile exists for the user
        Profile.objects.filter(user=self.user).delete()  # Clean up any existing profiles
        
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            description='Test Description'
            )
        self.task = Task.objects.create(
            creator = self.profile,
            title='test',
            due_date = timezone.make_aware(datetime.now()) + timedelta(days=7),
            )
    
    def test_tasks_list_url_seccessful_response(self):
        self.client.force_login(self.user)
        url = reverse('tasks:list_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list3.html')
        self.assertTrue(str(response.content).find('task') > 0)
        self.assertTrue(b'task' in response.content)
        
    def test_task_detail_logged_in_user(self):
        self.client.force_login(self.user)
        url = reverse('tasks:task-update', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)    
        
    def test_task_detail_logged_out_user(self):        
        url = reverse('tasks:task-update', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        



    