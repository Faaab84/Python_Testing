import pytest
from server import app, clubs, competitions



@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_data_before_each_test():
    """Remet les données à leur état initial avant chaque test."""
    _reset_les_donnees()


def _reset_les_donnees():
    """Fonction interne de réinitialisation des données."""
    for club in clubs:
        if club["name"] == "Simply Lift":
            club["points"] = "13"
        elif club["name"] == "Iron Temple":
            club["points"] = "4"
        elif club["name"] == "She Lifts":
            club["points"] = "12"

    for comp in competitions:
        if comp["name"] == "Spring Festival":
            comp["numberOfPlaces"] = "0"
        elif comp["name"] == "Classic0":
            comp["numberOfPlaces"] = "3"
        else:
            comp["numberOfPlaces"] = "25"



COMPETITION_OK = "Classic1"
COMPETITION_PASSEE = "Spring Festival"
COMPETITION_PEU_DE_PLACES = "Classic0"


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────
def test_champ_vide(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": COMPETITION_OK, "places": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
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
    for club in clubs:
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

    she_lifts = next((c for c in clubs if c["name"] == "She Lifts"), None)
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
