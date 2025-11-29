import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((c for c in clubs if c['email'] == email), None)
    if not club:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not club or not competition:
        flash("Something went wrong – please try again")
        return render_template('welcome.html', club=club or {}, competitions=competitions)

    try:
        comp_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        if comp_date < datetime.now():
            flash("You cannot book places for a past competition.")
            return render_template('welcome.html', club=club, competitions=competitions)
    except (ValueError, KeyError):
        flash("Something went wrong – please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

    try:
        placesRequired = int(request.form['places'])
        if placesRequired <= 0:
            raise ValueError
    except ValueError:
        flash("Please enter a valid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    club_points = int(club['points'])

    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
    elif placesRequired > club_points:
        flash(f"Not enough points – you only have {club_points} points available.")
    else:
        competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
        club['points'] = str(club_points - placesRequired)     #bug 5 fix with #bug 2
        flash("Great-booking complete!")

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/pointsDisplay')
def points_board():
    return render_template('points_board.html', clubs=clubs)

@app.route('/showSummary')
def showSummary_from_board():
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)