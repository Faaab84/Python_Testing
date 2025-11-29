import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from server import app
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_email_invalide(client):
    response = client.post(
        '/showSummary',
        data={'email': 'fabien@test.com'},
        follow_redirects=True
    )
    assert response.status_code == 200

    page = response.data.decode('utf-8')

    assert "Sorry" in page
    assert "Sorry, that email wasn&#39;t found." in page

    print("\n[ERREUR] Email invalide → message bien affiché")


def test_email_valide(client):
    response = client.post(
        '/showSummary',
        data={'email': 'admin@irontemple.com'},
        follow_redirects=True
    )
    assert response.status_code == 200

    page = response.data.decode('utf-8')
    assert "Welcome, admin@irontemple.com" in page
    assert "Désolé" not in page

    print("[SUCCÈS] Email valide → connexion OK")
