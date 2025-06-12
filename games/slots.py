# games/slots.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from db import get_user_by_id, update_balance, record_spin
import random

slots_bp = Blueprint('slots', __name__, url_prefix='/slots')

SYMBOLS = ['🍒', '💎', '7️⃣', '🍋', '🔔']
PAYOUTS = {
    ('🍒', '🍒', '🍒'): 5,
    ('💎', '💎', '💎'): 10,
    ('7️⃣', '7️⃣', '7️⃣'): 20,
    ('🍋', '🍋', '🍋'): 4,
    ('🔔', '🔔', '🔔'): 7
}

@slots_bp.route('/')
def play():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = get_user_by_id(session['user_id'])
    return render_template('slots.html', user=user)

@slots_bp.route('/spin', methods=['POST'])
def spin():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in."})

    bet = int(request.form['bet'])
    user = get_user_by_id(session['user_id'])

    if not user or user[2] < bet or bet <= 0:
        return jsonify({"error": "Invalid bet."})

    update_balance(user[0], -bet)
    result = tuple(random.choice(SYMBOLS) for _ in range(3))
    payout = PAYOUTS.get(result, 0) * bet
    update_balance(user[0], payout)
    record_spin(user[0], payout)

    user = get_user_by_id(user[0])  # Refresh balance

    return jsonify({
        "result": result,
        "payout": payout,
        "balance": user[2]
    })



