from django.urls import reverse
from django.test import TestCase
from accounts.models import User
from rest_framework import status

asssert 
class TestTaskApi(TestCase):

    def setUp(self):
        self.common_user = User.objects.create_user(id=100, email="t@test.com", password="T@pass123")
        self.client.login(email="t@test.com", password="T@pass123")

    def test_create_task_valid_data_response_201_status(self):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)  # Check if ID is present in the response

    def test_create_task_invalid_data_response_400_status(self):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)  # Validate that the error is related to title

    def test_update_task_valid_data_response_200_status(self):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        response = self.client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        updated_data = {
            "title": "test_updated",
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "test_updated")  # Ensure the title was updated

    def test_update_task_invalid_data_response_400_status(self):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        response = self.client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        updated_data = {
            "title": "",
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)  # Validate that the error is related to title

    def test_delete_task_response_204_status(self):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        response = self.client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)  # Ensure the task is deleted
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_get_create_task_response_200_status(self):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        response = self.client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "test")
        self.assertEqual(response.data["id"], task_id)
        self.assertEqual(response.data["creator"], self.common_user.id)

    def test_get_task_response_404_status(self):
        url = reverse("tasks:api-v1:task-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {})  # Ensure the response is empty for a non-existent task