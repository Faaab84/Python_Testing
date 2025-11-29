import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    """Load the list of clubs from clubs.json file."""
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    """Load the list of competitions from competitions.json file."""
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

# Load data when the app starts
competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """Show the home page with the login form."""
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """Check the email and show the welcome page if the club exists."""
    email = request.form['email']
    club = next((c for c in clubs if c['email'] == email), None)
    if not club:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """Show the booking page for a specific competition and club."""
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """Handle the booking of places. Check all rules before confirming."""
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Something went wrong – please try again")
        return render_template('welcome.html', club=club or {}, competitions=competitions)

    # Check if competition is in the past
    try:
        comp_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        if comp_date < datetime.now():
            flash("You cannot book places for a past competition.")
            return render_template('welcome.html', club=club, competitions=competitions)
    except (ValueError, KeyError, TypeError):
        flash("Something went wrong – please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Check if the number of places is valid
    places_str = request.form['places'].strip()
    if not places_str or not places_str.isdigit() or int(places_str) <= 0:
        flash("Please enter a valid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    placesRequired = int(places_str)
    club_points = int(club['points'])
    places_available = int(competition['numberOfPlaces'])

    # Check all booking rules
    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
    elif placesRequired > club_points:
        flash(f"Not enough points – you only have {club_points}.")
    elif placesRequired > places_available:
        flash(f"Not enough places available – only {places_available} left.")
    else:
        # Booking is valid → update points and places
        competition['numberOfPlaces'] = str(places_available - placesRequired)
        club['points'] = str(club_points - placesRequired)
        flash("Great-booking complete!")

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    """Log out and go back to the login page."""
    return redirect(url_for('index'))


@app.route('/pointsDisplay')
def points_board():
    """Show the page with all clubs and their points."""
    return render_template('points_board.html', clubs=clubs)


@app.route('/showSummary')
def showSummary_from_board():
    """Redirect to home page when clicking from the points board."""
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
