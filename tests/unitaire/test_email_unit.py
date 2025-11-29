import pytest

CLUBS = [
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
]


def rechercher_email(email):
    for club in CLUBS:
        if club['email'] == email:
            return club
    return None


def test_email_pas_trouve():
    result = rechercher_email("fabien@faux.com")
    assert result is None
    print("\n[ERREUR] Email invalide")


def test_email_trouve():
    result = rechercher_email("admin@irontemple.com")
    assert result is not None
    assert result["name"] == "Iron Temple"
    print("[SUCCÈS] Email valide")