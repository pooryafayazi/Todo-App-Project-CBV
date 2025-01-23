from django.test import TestCase,SimpleTestCase
from datetime import datetime,timedelta
from ..forms import TaskForm


class TestTaskForm(TestCase):
    
    def test_task_form_valid_data(self):
        form = TaskForm(data={
            'title':'test',
            'due_date':datetime.now() + timedelta(days=7),
            'completed':False
            })
        self.assertTrue(form.is_valid())
    
    def test_task_form_no_data(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)