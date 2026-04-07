#!/usr/bin/env python3
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# قائمة الألعاب من مجلد Pepper_Therapy
games_dir = os.path.join(os.path.dirname(__file__), 'templates', 'games')
GAMES = [f.replace('.html', '') for f in os.listdir(games_dir) if f.endswith('.html')]
GAMES.sort()

@app.route('/')
def home():
    return render_template('games_menu.html', games=GAMES)

@app.route('/game/<game_id>')
def play_game(game_id):
    return render_template(f'games/{game_id}.html')

if __name__ == '__main__':
    print(f"🎮 {len(GAMES)} games available")
    app.run(host='0.0.0.0', port=5001, debug=True)
