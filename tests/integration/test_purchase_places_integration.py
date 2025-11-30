

import pytest
import importlib

@pytest.fixture(autouse=True)
def reload_server():
    import server
    importlib.reload(server)


@pytest.fixture
def client():
    import server
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        yield client



COMPETITION_OK = "Classic1"
COMPETITION_PASSEE = "Spring Festival"
COMPETITION_PEU_DE_PLACES = "Classic0"



def test_champ_vide(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": COMPETITION_OK, "places": ""},
        follow_redirects=True,
    )
    assert "Please enter a valid number of places" in response.get_data(as_text=True)
    print("Champ vide → OK")


def test_lettres_dans_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": COMPETITION_OK, "places": "toto"},
        follow_redirects=True,
    )
    assert "Please enter a valid number of places" in response.get_data(as_text=True)
    print("Lettres → OK")


def test_plus_de_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": COMPETITION_OK, "places": "15"},
        follow_redirects=True,
    )
    assert "You cannot book more than 12 places per competition" in response.get_data(as_text=True)
    print("Plus de 12 → OK")


def test_pas_assez_de_points(client):
    import server
    for club in server.clubs:
        if club["name"] == "Iron Temple":
            club["points"] = "2"
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": COMPETITION_OK, "places": "5"},
        follow_redirects=True,
    )
    assert "Not enough points" in response.get_data(as_text=True)
    print("Pas assez de points → OK")


def test_competition_passee(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": COMPETITION_PASSEE, "places": "3"},
        follow_redirects=True,
    )
    assert "You cannot book places for a past competition" in response.get_data(as_text=True)
    print("Compétition passée → OK")


def test_pas_assez_de_places_disponibles(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": COMPETITION_PEU_DE_PLACES, "places": "10"},
        follow_redirects=True,
    )
    assert "Not enough places available – only 3 left" in response.get_data(as_text=True)
    print("Pas assez de places → OK")


def test_reservation_reussie(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "She Lifts", "competition": COMPETITION_OK, "places": "8"},
        follow_redirects=True,
    )
    texte = response.get_data(as_text=True)
    assert "Great-booking complete!" in texte

    import server
    she_lifts = next((c for c in server.clubs if c["name"] == "She Lifts"), None)
    assert she_lifts is not None
    assert int(she_lifts["points"]) == 4
    print("Réservation réussie → OK")


def test_club_inconnu(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Club Fantôme", "competition": COMPETITION_OK, "places": "5"},
        follow_redirects=True,
    )
    assert "Something went wrong" in response.get_data(as_text=True)
    print("Club inconnu → OK")