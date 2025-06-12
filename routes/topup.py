from flask import Blueprint, request, redirect, session, url_for
from db import update_balance

topup_bp = Blueprint('topup', __name__)

@topup_bp.route('/topup', methods=['POST'])
def topup():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    try:
        amount = int(request.form['amount'])
        if amount > 0:
            update_balance(session['user_id'], amount)
    except:
        pass

    return redirect(request.referrer or url_for('home'))
