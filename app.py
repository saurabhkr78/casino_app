from flask import Flask, render_template, request, flash, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'
cash = 100

@app.route("/", methods=["GET", "POST"])
def index():
    global cash
    if request.method == "POST":
        bet = int(request.form["bet"])
        guess = int(request.form["guess"])

        if bet == 0 or bet > cash:
            flash('Invalid bet amount.')
            return redirect(url_for('index'))

        result, cash = play(bet, guess)
        if cash < 0:
            flash('You are out of cash! Please recharge to continue playing.')
            return redirect(url_for('recharge'))

        return render_template("index.html", result=result, cash=cash)
    
    return render_template("index.html", cash=cash)

@app.route("/recharge", methods=["GET", "POST"])
def recharge():
    global cash
    if request.method == "POST":
        recharge_amount = int(request.form["recharge_amount"])
        cash += recharge_amount
        if cash < 100:
            flash('Minimum total amount to continue playing is $100.')
            return redirect(url_for('recharge'))
        else:
            flash('Recharge successful! You can now continue playing.')
            return redirect(url_for('index'))
    return render_template("recharge.html", cash=cash)

def play(bet, guess):
    global cash
    cards = ['J', 'Q', 'K']
    random.shuffle(cards)

    if cards[guess - 1] == 'Q':
        cash += 3 * bet
        result = f"Woohoo! You Win ;) Result={cards} Total Cash=${cash}"
    else:
        cash -= 3 * bet
        result = f"Alas! You lost :( Result={cards} Total Cash=${cash}"
    
    return result, cash

if __name__ == "__main__":
    app.run(debug=True)
