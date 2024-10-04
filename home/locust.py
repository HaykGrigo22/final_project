from locust import HttpUser, task, between


class StressTest(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.get("/login/")
        csrftoken = response.cookies['csrftoken']

        self.client.post("/login/", data={"email": "haykgrigo22@gmail.com", "password": "1234"},
                         headers={"X-CSRFToken": csrftoken})

    @task
    def home_task(self):
        self.client.get("")
        self.client.get("advanced-search")
        self.client.get("about-us")

