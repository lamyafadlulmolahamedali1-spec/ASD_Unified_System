#!/usr/bin/env python3
"""
Enhanced Games Integration - مع أصوات تشجيعية وربط النقاط
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
import random
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'asd_secret_key_2024'

DATA_DIR = '/home/lamya/Desktop/ASD_Complete_Project_20260325_161142/data'
os.makedirs(DATA_DIR, exist_ok=True)

# ==================== Games List ====================
games_dir = os.path.join(os.path.dirname(__file__), 'templates', 'games')
GAMES_LIST = []
if os.path.exists(games_dir):
    for f in os.listdir(games_dir):
        if f.endswith('.html') and f not in ['landing.html', 'parent_login.html', 'child_login.html', 'games_menu.html', 'parent_dashboard.html']:
            GAMES_LIST.append(os.path.splitext(f)[0])
GAMES_LIST = list(set(GAMES_LIST))
GAMES_LIST.sort()

ICONS = {
    'aba_matching': '🎯', 'aba_sorting': '📊', 'alphabet_song': '🎵', 'animal_sounds': '🐶',
    'ball_sort_perfect': '⚾', 'block_blast': '🧩', 'brain_oddone': '🤔', 'brain_pattern': '🔄',
    'color_match': '🎨', 'coloring_game': '🖍️', 'crossword_english': '📝', 'daily_routine': '⏰',
    'do_dont': '✅', 'drawing_pad': '✏️', 'emotion_match': '😊', 'familiar_things': '🏠',
    'language_game': '💬', 'letter_coloring': '🔤', 'math_challenge': '🔢', 'memory_cards': '🎴',
    'memory_game': '🧠', 'music_rhythm': '🎵', 'pepper_emotions': '😊', 'pepper_imitation': '🤖',
    'physical_activity': '🏃', 'sensory_bubbles': '🫧', 'sensory_fireworks': '🎆', 'sensory_spinner': '🌀',
    'shape_sorting': '⭐', 'smart_alarm': '⏰', 'snake_game': '🐍', 'social_stories_english': '📖',
    'spot_difference': '🔍', 'story_library_full': '📚', 'sudoku': '🔢', 'teacch_schedule': '📋',
    'teacch_work': '⚙️', 'tictactoe_game': '❌', 'word_search': '🔍', 'work_system': '🔧',
    'color_sort': '🎨', 'counting': '🔢'
}

# ==================== Data Management ====================
def load_data():
    parents_file = os.path.join(DATA_DIR, 'parents.json')
    children_file = os.path.join(DATA_DIR, 'children.json')
    progress_file = os.path.join(DATA_DIR, 'progress.json')
    
    if not os.path.exists(parents_file):
        with open(parents_file, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(children_file):
        with open(children_file, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(progress_file):
        with open(progress_file, 'w') as f:
            json.dump({}, f)
    
    with open(parents_file, 'r') as f:
        parents = json.load(f)
    with open(children_file, 'r') as f:
        children = json.load(f)
    with open(progress_file, 'r') as f:
        progress = json.load(f)
    
    return parents, children, progress

def save_data(parents, children, progress):
    parents_file = os.path.join(DATA_DIR, 'parents.json')
    children_file = os.path.join(DATA_DIR, 'children.json')
    progress_file = os.path.join(DATA_DIR, 'progress.json')
    
    with open(parents_file, 'w') as f:
        json.dump(parents, f, indent=2)
    with open(children_file, 'w') as f:
        json.dump(children, f, indent=2)
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)

# ==================== Update Game Score ====================
@app.route('/api/update_score', methods=['POST'])
def update_score():
    data = request.json
    child_name = data.get('child_name')
    game_name = data.get('game_name')
    score = data.get('score', 10)
    correct = data.get('correct', True)
    
    if not child_name or not game_name:
        return jsonify({'status': 'error', 'message': 'Missing data'})
    
    parents, children, progress = load_data()
    
    if child_name not in progress:
        progress[child_name] = {'games': {}, 'total_points': 0, 'games_played': 0, 'attention': 75, 'tasks_completed': 0}
    
    if game_name not in progress[child_name]['games']:
        progress[child_name]['games'][game_name] = 0
    
    progress[child_name]['games'][game_name] += score
    progress[child_name]['total_points'] += score
    progress[child_name]['games_played'] += 1
    
    save_data(parents, children, progress)
    
    # Return encouraging message
    messages = [
        "🎉 Great job! You earned points!",
        "🌟 Excellent work! Keep going!",
        "⭐ You're doing amazing!",
        "💪 Fantastic! You're learning so well!"
    ]
    
    return jsonify({'status': 'success', 'points': score, 'message': random.choice(messages)})

# ==================== Game Template with Sound ====================
GAME_WRAPPER = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ game_name }} - ASD Game</title>
    <style>
        body {{
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
            min-height: 100vh;
        }}
        .game-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
        }}
        h1 {{ color: #e94560; text-align: center; }}
        .back-btn {{
            background: #e94560;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin-bottom: 20px;
        }}
        .game-content {{
            min-height: 400px;
        }}
        .message-area {{
            margin-top: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
        }}
        button {{
            background: #e94560;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin: 5px;
        }}
        .correct-answer {{
            background: #4caf50;
            animation: celebrate 0.5s ease;
        }}
        .wrong-answer {{
            background: #f44336;
            animation: shake 0.3s ease;
        }}
        @keyframes celebrate {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); background: #66bb6a; }}
            100% {{ transform: scale(1); }}
        }}
        @keyframes shake {{
            0%,100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <button class="back-btn" onclick="window.location.href='/child/dashboard'">← Back to Dashboard</button>
        <h1>{{ game_title }}</h1>
        <div class="game-content" id="gameContent">
            <p style="text-align: center; padding: 50px;">Loading game... Make sure this is a real game template.</p>
        </div>
        <div class="message-area" id="messageArea">
            💡 Play the game and earn points!
        </div>
    </div>
    
    <script>
        let currentChild = localStorage.getItem('current_child') || '{{ child_name }}';
        
        function playSound(type) {{
            const sounds = {{
                correct: ['👏', '🎉', '🌟', '⭐', '💪'],
                wrong: ['😊', '👍', '💪', '📚', '🌱']
            }};
            const emoji = sounds[type][Math.floor(Math.random() * sounds[type].length)];
            const msgDiv = document.getElementById('messageArea');
            if (type === 'correct') {{
                msgDiv.innerHTML = `${emoji} Great job! +10 points! ${emoji}`;
                msgDiv.style.background = '#4caf50';
                setTimeout(() => {{ msgDiv.style.background = 'rgba(0,0,0,0.5)'; }}, 1500);
                updateScore(10, true);
            }} else {{
                msgDiv.innerHTML = `${emoji} Good try! Keep practicing! ${emoji}`;
                msgDiv.style.background = '#ff9800';
                setTimeout(() => {{ msgDiv.style.background = 'rgba(0,0,0,0.5)'; }}, 1500);
                updateScore(2, false);
            }}
        }}
        
        function updateScore(points, correct) {{
            fetch('/api/update_score', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    child_name: currentChild,
                    game_name: '{{ game_id }}',
                    score: points,
                    correct: correct
                }})
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.status === 'success') {{
                    console.log('Score updated:', data.points);
                }}
            }});
        }}
        
        // Expose functions to child game
        window.onCorrectAnswer = function() {{ playSound('correct'); }};
        window.onWrongAnswer = function() {{ playSound('wrong'); }};
        
        // Load the actual game
        fetch('/game_content/{{ game_id }}')
            .then(res => res.text())
            .then(html => {{
                document.getElementById('gameContent').innerHTML = html;
                // Inject sound functions into the game
                setTimeout(() => {{
                    if (typeof window.injectSoundHandlers === 'function') {{
                        window.injectSoundHandlers(playSound, updateScore);
                    }}
                }}, 100);
            }})
            .catch(() => {{
                document.getElementById('gameContent').innerHTML = `
                    <div style="text-align: center; padding: 50px;">
                        <h2>{{ game_title }}</h2>
                        <p>Game content would appear here.</p>
                        <button onclick="window.location.href='/child/dashboard'">Back to Games</button>
                    </div>
                `;
            }});
    </script>
</body>
</html>
'''

# ==================== Routes ====================
@app.route('/game/<game_name>')
def play_game(game_name):
    child_name = session.get('child', 'Child')
    game_title = game_name.replace('_', ' ').title()
    return render_template_string(GAME_WRAPPER, 
                                  game_name=game_name, 
                                  game_title=game_title, 
                                  game_id=game_name,
                                  child_name=child_name)

@app.route('/game_content/<game_name>')
def game_content(game_name):
    try:
        from flask import render_template
        return render_template(f'games/{game_name}.html')
    except:
        return f'<div style="text-align:center; padding:50px;"><h2>{game_name.replace("_", " ").title()}</h2><p>Game content would be here.</p><button onclick="window.location.href=\'/child/dashboard\'">Back</button></div>'

# Simple landing for testing
@app.route('/')
def landing():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>ASD System</title>
    <style>
        body { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; font-family: Arial; text-align: center; padding: 50px; }
        .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: #e94560; border-radius: 10px; text-decoration: none; color: white; }
    </style>
    </head>
    <body>
        <h1>🧩 ASD Support System</h1>
        <a href="/child/dashboard" class="btn">🧒 Child Dashboard</a>
        <a href="/parent/dashboard" class="btn">👨‍👩‍👧 Parent Dashboard</a>
    </body>
    </html>
    '''

# Child Dashboard (simplified for testing)
@app.route('/child/dashboard')
def child_dashboard():
    if 'child' not in session:
        session['child'] = 'Child'
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>Child Dashboard</title>
    <style>
        body {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; font-family: Arial; padding: 20px; }}
        .games-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; }}
        .game-card {{ background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; text-align: center; cursor: pointer; transition: 0.3s; }}
        .game-card:hover {{ background: #e94560; transform: scale(1.05); }}
        .back-btn {{ background: #e94560; border: none; padding: 10px 20px; border-radius: 10px; color: white; cursor: pointer; margin-bottom: 20px; }}
    </style>
    </head>
    <body>
        <button class="back-btn" onclick="window.location.href='/'">← Back</button>
        <h1>🎮 My Games</h1>
        <div class="games-grid" id="gamesGrid"></div>
        <script>
            const games = {json.dumps(GAMES_LIST)};
            const icons = {json.dumps(ICONS)};
            const grid = document.getElementById('gamesGrid');
            games.forEach(game => {{
                const card = document.createElement('div');
                card.className = 'game-card';
                card.innerHTML = `<div style="font-size:48px;">${{icons[game] || '🎮'}}</div><div>${{game.replace(/_/g, ' ')}}</div>`;
                card.onclick = () => window.location.href = `/game/${{game}}`;
                grid.appendChild(card);
            }});
        </script>
    </body>
    </html>
    '''

# Parent Dashboard
@app.route('/parent/dashboard')
def parent_dashboard():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Parent Dashboard</title>
    <style>
        body { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; font-family: Arial; padding: 20px; }
        .card { background: rgba(255,255,255,0.1); border-radius: 20px; padding: 20px; margin-bottom: 20px; }
        .games-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px; }
        .game-card { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px; text-align: center; }
        .stat { display: flex; justify-content: space-between; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 10px; margin: 5px 0; }
    </style>
    </head>
    <body>
        <h1>👨‍👩‍👧 Parent Dashboard</h1>
        <div class="card">
            <h2>📊 Child Progress</h2>
            <div id="progress"></div>
        </div>
        <div class="card">
            <h2>🎮 Games Played</h2>
            <div id="gamesPlayed" class="games-grid"></div>
        </div>
        <button onclick="location.reload()">Refresh</button>
        <script>
            function loadProgress() {
                fetch('/api/child_progress')
                    .then(res => res.json())
                    .then(data => {
                        const progressDiv = document.getElementById('progress');
                        progressDiv.innerHTML = `
                            <div class="stat"><span>🎯 Attention Score:</span><span>${data.attention}%</span></div>
                            <div class="stat"><span>🎮 Games Played:</span><span>${data.games_played}</span></div>
                            <div class="stat"><span>⭐ Total Points:</span><span>${data.total_points}</span></div>
                        `;
                        
                        const gamesDiv = document.getElementById('gamesPlayed');
                        gamesDiv.innerHTML = '';
                        for (let [game, score] of Object.entries(data.games)) {
                            if (score > 0) {
                                gamesDiv.innerHTML += `<div class="game-card"><div>${game.replace(/_/g, ' ')}</div><div style="color:#e94560;">⭐ ${score}</div></div>`;
                            }
                        }
                        if (gamesDiv.innerHTML === '') gamesDiv.innerHTML = '<p>No games played yet.</p>';
                    });
            }
            loadProgress();
            setInterval(loadProgress, 5000);
        </script>
    </body>
    </html>
    '''

@app.route('/api/child_progress')
def child_progress():
    _, children, progress = load_data()
    child_name = 'Child'
    child_data = progress.get(child_name, {'games': {}, 'total_points': 0, 'games_played': 0, 'attention': 75})
    return jsonify({
        'attention': child_data.get('attention', 75),
        'games_played': child_data.get('games_played', 0),
        'total_points': child_data.get('total_points', 0),
        'games': child_data.get('games', {})
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎮 Enhanced Games System")
    print("="*50)
    print("✅ Games with sound effects")
    print("✅ Points tracked to Parent Dashboard")
    print(f"🎮 Games available: {len(GAMES_LIST)}")
    print("="*50)
    print("🌐 Opening at: http://localhost:5001")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
