import pytest
from server import app, clubs, competitions



def reset_les_donnees():
    for club in clubs:
        if club["name"] == "Simply Lift":
            club["points"] = "13"
        elif club["name"] == "Iron Temple":
            club["points"] = "4"
        elif club["name"] == "She Lifts":
            club["points"] = "12"
COMPETITION_OK = "Classic1"
COMPETITION_PASSEE = "Spring Festival"
COMPETITION_PEU_DE_PLACES = "Classic0"


def test_champ_vide():
    reset_les_donnees()
    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': COMPETITION_OK,
            'places': ''
        }, follow_redirects=True)
        texte = reponse.data.decode()
        assert "Please enter a valid number of places" in texte
        print("Champ vide → OK")


def test_lettres_dans_places():
    reset_les_donnees()
    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': COMPETITION_OK,
            'places': 'toto'
        }, follow_redirects=True)
        texte = reponse.data.decode()
        assert "Please enter a valid number of places" in texte
        print("Lettres → OK")


def test_plus_de_12_places():
    reset_les_donnees()
    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': COMPETITION_OK,
            'places': '15'
        }, follow_redirects=True)
        texte = reponse.data.decode()
        assert "You cannot book more than 12 places per competition" in texte
        print("Plus de 12 → OK")


def test_pas_assez_de_points():
    reset_les_donnees()
    for club in clubs:
        if club["name"] == "Iron Temple":
            club["points"] = "2"

    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': COMPETITION_OK,
            'places': '5'
        }, follow_redirects=True)
        texte = reponse.data.decode()
        assert "Not enough points" in texte
        print("Pas assez de points → OK")


def test_competition_passee():
    reset_les_donnees()
    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': COMPETITION_PASSEE,
            'places': '3'
        }, follow_redirects=True)
        texte = reponse.data.decode()
        assert "You cannot book places for a past competition" in texte
        print("Compétition passée → OK")


def test_pas_assez_de_places_disponibles():
    reset_les_donnees()
    for comp in competitions:
        if comp["name"] == "Classic0":
            comp["numberOfPlaces"] = "3"

    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': COMPETITION_PEU_DE_PLACES,
            'places': '10'
        }, follow_redirects=True)
        texte = reponse.data.decode()
        assert "Not enough places available – only 3 left" in texte
        print("Pas assez de places → OK")


def test_reservation_reussie():
    reset_les_donnees()
    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'She Lifts',
            'competition': COMPETITION_OK,
            'places': '8'
        }, follow_redirects=True)
        texte = reponse.data.decode()
        she_lifts = None
        for club in clubs:
            if club["name"] == "She Lifts":
                she_lifts = club
                break
        assert "Great-booking complete!" in texte
        assert she_lifts["points"] == "4"
        print("Réservation réussie → OK")


def test_club_inconnu():
    reset_les_donnees()
    with app.test_client() as client:
        reponse = client.post('/purchasePlaces', data={
            'club': 'Club Fantôme',
            'competition': COMPETITION_OK,
            'places': '5'
        }, follow_redirects=True)
        texte = reponse.data.decode()
        assert "Something went wrong" in texte
        print("Club inconnu → OK")
