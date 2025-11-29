from locust import HttpUser, task, between


class SecretaryUser(HttpUser):
    wait_time = between(1, 5)

    @task(4)
    def book_competition_success(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        self.client.get("/book/Spring%20Festival/Simply%20Lift")
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "3"
        })
        self.client.get("/logout")

    @task(2)
    def book_with_not_enough_points(self):
        self.client.post("/showSummary", data={"email": "admin@irontemple.com"})
        self.client.get("/book/Spring%20Festival/Iron%20Temple")
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "10"
        })
        self.client.get("/logout")

    @task(2)
    def try_too_many_places(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        self.client.get("/book/Spring%20Festival/Simply%20Lift")
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "20"
        })
        self.client.get("/logout")

    @task(3)
    def view_points_board(self):
        self.client.post("/showSummary", data={"email": "kate@shelifts.co.uk"})
        self.client.get("/pointsDisplay")
        self.client.get("/logout")
