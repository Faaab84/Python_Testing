from locust import HttpUser, task, between
import random

VALID_EMAILS = [
    "john@simplylift.co",
    "admin@irontemple.com",  #
    "kate@shelifts.co.uk"
]

FUTURE_COMPETITIONS = [
    "Classic1",
    "Classic0",
    "Classic"
]


class GUDLFTUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):

        email = random.choice(VALID_EMAILS)
        response = self.client.post("/showSummary", data={"email": email}, allow_redirects=True)
        if "Welcome" not in response.text:
            print(f"Connexion échouée pour {email}")
        else:
            print(f"Connecté avec {email}")

    @task(3)
    def view_competitions(self):

        self.client.get("/")

    @task(5)
    def book_places_valid(self):

        competition = random.choice(FUTURE_COMPETITIONS)
        places = random.randint(1, 10)


        self.client.get(f"/book/{competition.strip()}/Simply Lift")


        response = self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": competition,
            "places": str(places)
        }, allow_redirects=True)

        if "Great-booking complete!" in response.text:
            print(f"Réservation de {places} places sur {competition} → OK")
        elif "You cannot book more than 12 places" in response.text:
            print(f"Tentative de trop de places bloquée → OK")
        elif "Not enough points" in response.text:
            print("Pas assez de points → OK (normal)")

    @task(1)
    def try_book_too_many_places(self):
        self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Classic1",
            "places": "20"
        })

    @task(2)
    def view_points_board(self):
        self.client.get("/pointsDisplay")