from flask import Flask, render_template, request, flash, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'
cash = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global cash
    if request.method == "POST":
        if 'recharge_amount' in request.form:
            recharge_amount = int(request.form["recharge_amount"])
            cash = recharge_amount
            flash('Recharge successful! You can now enter the game.')
            return redirect(url_for('index'))
        else:
            bet = int(request.form["bet"])
            card = request.form["card"]
            guess = int(request.form["guess"])

            if bet <= 0 or bet > cash:
                flash('Invalid bet amount.')
                return redirect(url_for('index'))

            result = play(bet, card, guess)
            if "You lost" in result:
                flash("You lost the bet")
            return render_template("index.html", result=result, cash=cash)

    return render_template("index.html", cash=cash)

def play(bet, card, guess):
    global cash
    cards = [card, 'Q', 'K'] if card != 'Q' else ['J', 'Q', 'K']
    random.shuffle(cards)

    if cards[guess - 1] == 'Q':
        cash += 2 * bet
        result = f"Woohoo! You Win ;) Result={cards} Total Cash=${cash}"
    else:
        cash -= bet
        result = f"Alas! You lost :( Result={cards} Total Cash=${cash}"
    
    return result

if __name__ == "__main__":
    app.run(debug=True)
