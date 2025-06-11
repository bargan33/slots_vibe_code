from flask import Flask, render_template, request, jsonify, session
import random
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'slot-secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

SYMBOLS = ['🍒', '💎', '7️⃣', '🍋', '🔔']
PAYOUTS = {
    ('🍒', '🍒', '🍒'): 5,
    ('💎', '💎', '💎'): 10,
    ('7️⃣', '7️⃣', '7️⃣'): 20,
    ('🍋', '🍋', '🍋'): 4,
    ('🔔', '🔔', '🔔'): 7
}

@app.route('/')
def index():
    if 'balance' not in session:
        session['balance'] = 100
    return render_template('index.html', balance=session['balance'])

@app.route('/spin', methods=['POST'])
def spin():
    bet = int(request.form['bet'])
    if session['balance'] < bet or bet <= 0:
        return jsonify({"error": "Invalid bet."})

    session['balance'] -= bet
    result = tuple(random.choice(SYMBOLS) for _ in range(3))
    payout = PAYOUTS.get(result, 0) * bet
    session['balance'] += payout

    return jsonify({
        "result": result,
        "payout": payout,
        "balance": session['balance']
    })

if __name__ == '__main__':
    app.run(debug=True)