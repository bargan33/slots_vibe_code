from flask import Flask, render_template, session
from flask_session import Session
import os

from auth import auth_bp
from db import init_db, get_leaderboard, get_user_by_id
from games.slots import slots_bp
from routes.topup import topup_bp  # ✅ Import the new blueprint

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Init DB if not yet present
if not os.path.exists('casino.db'):
    init_db()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(slots_bp)
app.register_blueprint(topup_bp)  # ✅ Register the topup blueprint

@app.route('/')
def home():
    user = get_user_by_id(session['user_id']) if 'user_id' in session else None
    leaderboard = get_leaderboard()
    return render_template('index.html', user=user, leaderboard=leaderboard)

if __name__ == '__main__':
    app.run(debug=True)
