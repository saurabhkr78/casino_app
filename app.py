from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)
cash = 100

@app.route("/", methods=["GET", "POST"])
def index():
    global cash
    if request.method == "POST":
        bet = int(request.form["bet"])
        if bet == 0 or bet > cash:
            return redirect(url_for('index'))

        result, cash = play(bet)
        return render_template("index.html", result=result, cash=cash)
    
    return render_template("index.html", cash=cash)

def play(bet):
    global cash
    cards = ['J', 'Q', 'K']
    random.shuffle(cards)
    guess = int(request.form["guess"])

    if cards[guess - 1] == 'Q':
        cash += 3 * bet
        result = f"Woohoo! You Win ;) Result={cards} Total Cash=${cash}"
    else:
        cash -= 3 * bet
        result = f"Alas! You lost :( Result={cards} Total Cash=${cash}"
    
    return result, cash

if __name__ == "__main__":
    app.run(debug=True)
