from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from ..views import TasksListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskCompleteView

# Create your tests here.

class TestUrl(TestCase):
    
    def test_tasks_list_url(self):
        url = reverse('tasks:list_view')
        self.assertEqual(resolve(url).func.view_class, TasksListView)
        
    def test_task_create_url(self):
        url = reverse('tasks:task-create')
        self.assertEqual(resolve(url).func.view_class, TaskCreateView)
        
    def test_task_update_url(self):
        url = reverse('tasks:task-update', kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class, TaskUpdateView)
        
    def test_task_delete_url(self):
        url = reverse('tasks:task-delete', kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class, TaskDeleteView)
        
    def test_task_complete_url(self):
        url = reverse('tasks:task-complete', kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class, TaskCompleteView)