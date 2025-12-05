import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from unittest.mock import patch
from server import validate_booking

CLUB = {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "30"}
COMPETITION = {"name": "Classic", "date": "2026-10-22 13:30:00", "numberOfPlaces": "13"}

@patch('server.int')
def test_validate_booking_reussie(mock_int):
    mock_int.side_effect = [30, 13]
    club_copy = CLUB.copy()
    comp_copy = COMPETITION.copy()
    is_valid, message, updated_club, updated_comp = validate_booking(7, club_copy, comp_copy)
    mock_int.assert_any_call('30')
    mock_int.assert_any_call('13')
    assert is_valid is True
    assert message == "Great-booking complete!"
    print("Test 1 : réservation réussie avec mock → OK")

@patch('server.int')
def test_validate_booking_plus_12(mock_int):
    mock_int.side_effect = [30, 13]
    club_copy = CLUB.copy()
    comp_copy = COMPETITION.copy()
    is_valid, message, _, _ = validate_booking(15, club_copy, comp_copy)
    mock_int.assert_any_call('30')
    mock_int.assert_any_call('13')
    assert is_valid is False
    assert "12 places" in message
    print("Test 2 : plus de 12 places avec mock → OK")

@patch('server.int')
def test_validate_booking_pas_assez_points(mock_int):
    mock_int.side_effect = [5, 13]
    club_copy = CLUB.copy()
    comp_copy = COMPETITION.copy()
    is_valid, message, _, _ = validate_booking(10, club_copy, comp_copy)
    mock_int.assert_any_call('30')
    mock_int.assert_any_call('13')
    assert is_valid is False
    assert "Not enough points" in message
    print("Test 3 : pas assez points avec mock → OK")

@patch('server.int')
def test_validate_booking_pas_assez_places(mock_int):
    mock_int.side_effect = [30, 3]
    club_copy = CLUB.copy()
    comp_copy = {"name": "Classic0", "numberOfPlaces": "3"}.copy()
    is_valid, message, _, _ = validate_booking(5, club_copy, comp_copy)
    mock_int.assert_any_call('30')
    mock_int.assert_any_call('3')
    assert is_valid is False
    assert "only 3 left" in message
    print("Test 4 : pas assez places avec mock → OK")

