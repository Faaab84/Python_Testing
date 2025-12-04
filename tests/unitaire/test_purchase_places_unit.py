import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from server import app
from unittest.mock import patch

COMPETITIONS = [
    {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
    {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
    {"name": "Classic", "date": "2026-10-22 13:30:00", "numberOfPlaces": "13"},
    {"name": "Classic0", "date": "2026-10-22 13:30:00", "numberOfPlaces": "3"},
    {"name": "Classic1", "date": "2026-10-23 13:30:00", "numberOfPlaces": "100"},
]

CLUB = {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "30"}


@patch('server.clubs', new_callable=list)
@patch('server.competitions', new_callable=list)
def test_reservation_reussie_points_deduits(mock_competitions, mock_clubs):

    club_copy = CLUB.copy()
    club_copy["points"] = "20"
    mock_clubs[:] = [club_copy]
    mock_competitions[:] = COMPETITIONS

    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Classic',
            'places': '7'
        })

    assert b"Great" in response.data
    assert b"booking" in response.data
    assert club_copy["points"] == "13"
    print("Réservation réussie → points déduits → OK")


@patch('server.loadClubs')
@patch('server.loadCompetitions')
def test_plus_de_12_places_refusee(mock_comp, mock_clubs):
    mock_clubs.return_value = [CLUB]
    mock_comp.return_value = COMPETITIONS
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Classic1',
            'places': '15'
        })
    assert b"cannot book more than 12" in response.data or b"12 places" in response.data
    print("Plus de 12 places → refusée → OK")


@patch('server.loadClubs')
@patch('server.loadCompetitions')
def test_competition_passee_refusee(mock_comp, mock_clubs):
    mock_clubs.return_value = [CLUB]
    mock_comp.return_value = COMPETITIONS
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': '5'
        })
    assert b"past competition" in response.data
    print("Compétition passée → refusée → OK")


@patch('server.loadClubs')
@patch('server.loadCompetitions')
def test_pas_assez_de_points_refusee(mock_comp, mock_clubs):
    club_copy = CLUB.copy()
    club_copy["points"] = "5"
    mock_clubs.return_value = [club_copy]
    mock_comp.return_value = COMPETITIONS
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Classic',
            'places': '10'
        })
    assert b"Not enough points" in response.data
    print("Pas assez de points → refusée → OK")


@patch('server.loadClubs')
@patch('server.loadCompetitions')
def test_pas_assez_de_places_disponibles(mock_comp, mock_clubs):
    mock_clubs.return_value = [CLUB]
    mock_comp.return_value = COMPETITIONS
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Classic0',
            'places': '5'
        })
    assert b"only" in response.data and b"left" in response.data
    print("Pas assez de places → refusée → OK")
