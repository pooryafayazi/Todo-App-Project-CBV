from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from accounts.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_user():
    user = User.objects.create_user(id=100, email="t@test.com", password="T@pass123")
    return user


@pytest.mark.django_db
class TestTaskApi:

    def test_get_task_response_200_status(self, api_client):
        api_client.force_authenticate(user=None)
        url = reverse("tasks:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_401_status(self, api_client):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        api_client.force_authenticate(user=None)
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_task_valid_data_response_201_status(self, api_client, common_user):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_task_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        api_client.force_login(user=common_user)
        
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_update_task_response_401_status(self, api_client):
        url = reverse("tasks:api-v1:task-detail", args=[1])
        data = {
            "title": "test",
        }
        api_client.force_authenticate(user=None)
        response = api_client.put(url, data)
        assert response.status_code == 401

    def test_update_task_valid_data_response_200_status(self, api_client, common_user):
        api_client.force_login(user=common_user)
        
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        response = api_client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        data = {
            "title": "test_updated",
        }
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_update_task_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        data = {
            "title": "",
        }
        response = api_client.put(url, data)
        assert response.status_code == 400

    def test_delete_task_response_401_status(self, api_client):
        url = reverse("tasks:api-v1:task-detail", args=[1])
        api_client.force_authenticate(user=None)
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_delete_task_response_204_status(self, api_client, common_user):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_post_get_create_task_response_200_status(self, api_client, common_user):
        url = reverse("tasks:api-v1:task-list")
        data = {
            "title": "test",
        }
        api_client.force_login(user=common_user)
        response = api_client.post(url, data)
        task_id = response.data["id"]
        url = reverse("tasks:api-v1:task-detail", args=[task_id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["title"] == "test"
        assert response.data["id"] == task_id
        assert response.data["creator"] == common_user.id

    def test_get_task_response_404_status(self, api_client, common_user):
        url = reverse("tasks:api-v1:task-detail", args=[1])
        api_client.force_login(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 404
