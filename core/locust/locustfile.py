from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

    def on_start(self):
        resopnse = self.client.post("/accounts/api/v1/jwt/create/", data={
            "email": "admin@admin.com",
            "password": "123"}).json()
        self.client.headers = {'Authorization': f'Bearer {resopnse.get("access",None)}'}

    @task
    def task_list(self):
        self.client.get("/api/v1/task/")
