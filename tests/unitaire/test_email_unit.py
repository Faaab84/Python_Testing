import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from unittest.mock import patch, MagicMock
from server import find_club_by_email

CLUBS = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}
]


@patch('server.next')
def test_find_club_by_email_valide(mock_next):
    mock_club = {"name": "Simply Lift"}
    mock_next.return_value = mock_club

    result = find_club_by_email('john@simplylift.co', CLUBS)

    mock_next.assert_called_once()
    assert result['name'] == 'Simply Lift'
    print("Test 1 : email valide avec mock → OK")


@patch('server.next')
def test_find_club_by_email_invalide(mock_next):
    mock_next.return_value = None

    result = find_club_by_email('fabien.balaramane@outlook.fr', CLUBS)

    mock_next.assert_called_once()
    assert result is None
    print("Test 2 : email invalide avec mock → OK")
