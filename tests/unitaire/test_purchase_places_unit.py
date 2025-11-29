
from datetime import datetime

COMPETITIONS = [
    {"name": "Spring Festival", "date": "2026-03-27 10:00:00", "numberOfPlaces": "25"},
    {"name": "Fall Classic",    "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
    {"name": "Tiny Comp",       "date": "2026-11-01 14:00:00", "numberOfPlaces": "3"},
    {"name": "Big Comp",        "date": "2026-12-10 10:00:00", "numberOfPlaces": "100"},
]

CLUB = {"name": "Iron Temple", "points": "30"}

def reserver(competition_name, places):

    competition = None
    for comp in COMPETITIONS:
        if comp["name"] == competition_name:
            competition = comp
            break
    if not competition:
        return False, "Compétition inconnue"

    try:
        comp_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        if comp_date < datetime.now():
            return False, "Compétition passée"
    except:
        return False, "Date invalide"

    if places > 12:
        return False, "Max 12 places"
    if places > int(CLUB["points"]):
        return False, "Not enough points"
    if places > int(competition["numberOfPlaces"]):
        return False, "Not enough places available"

    competition["numberOfPlaces"] = str(int(competition["numberOfPlaces"]) - places)
    CLUB["points"] = str(int(CLUB["points"]) - places)
    return True, "Booking complete"


# ===================== TESTS =====================

def test_plus_de_12_places_refuse():
    CLUB["points"] = "30"
    success, msg = reserver("Big Comp", 15)
    assert success is False
    assert "Max 12 places" in msg
    print("Plus de 12 places → refusée")

def test_12_places_acceptee():
    CLUB["points"] = "30"
    success, msg = reserver("Big Comp", 12)
    assert success is True
    assert CLUB["points"] == "18"
    print("12 places → acceptée")

def test_pas_assez_de_points():
    CLUB["points"] = "8"
    success, msg = reserver("Spring Festival", 10)
    assert success is False
    assert "Not enough points" in msg
    print("Pas assez de points → refusée")

def test_competition_passee():
    CLUB["points"] = "30"
    success, msg = reserver("Fall Classic", 5)
    assert success is False
    print("Compétition passée → impossible")

def test_pas_assez_de_places_disponibles():
    CLUB["points"] = "30"
    success, msg = reserver("Tiny Comp", 5)
    assert success is False
    print("Plus de places que disponibles → refusée")

def test_reservation_ok():
    CLUB["points"] = "30"
    success, msg = reserver("Spring Festival", 7)
    assert success is True
    assert CLUB["points"] == "23"
    print("Réservation normale → OK")
