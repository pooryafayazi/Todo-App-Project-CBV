from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
 
# User = get_user_model()

class Task(models.Model):
    creator = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_snippet(self):
        return self.title[0:4]
    def get_absolute_api_url(self,**kwargs):
        return reverse('tasks:api-v1:task-detail', kwargs={'pk': self.pk})
        # return f"/api/v1/task/{self.id}/"

    class Meta:
        order_with_respect_to = "creator"