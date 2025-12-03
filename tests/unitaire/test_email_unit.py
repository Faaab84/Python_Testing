import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from server import app
from unittest.mock import patch

CLUBS = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
]


@patch('server.loadClubs')
def test_email_valide_affiche_page_bienvenue(mock_load_clubs):
    mock_load_clubs.return_value = CLUBS

    with app.test_client() as client:
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'john@simplylift.co' in response.data

    print("Test 1 : email valide → OK")


@patch('server.loadClubs')
def test_email_invalide_ou_vide_affiche_message_erreur(mock_load_clubs):
    mock_load_clubs.return_value = CLUBS  # même liste !

    with app.test_client() as client:
        rep1 = client.post('/showSummary', data={'email': 'fabien.balaramane@outlook.fr'}, follow_redirects=True)

        rep2 = client.post('/showSummary', data={'email': ''}, follow_redirects=True)

        assert b'Sorry' in rep1.data
        assert b'Sorry' in rep2.data

    print("Test 2 : email invalide ou vide → OK")
