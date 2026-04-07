#!/usr/bin/env python3
"""
ASD Complete Dashboard - Dual System
- Parent Dashboard (مراقبة التقدم)
- Child Dashboard (ألعاب + تمارين)
- Autism Support Chatbot
- Progress Tracking
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

# ==================== Autism Knowledge Base ====================
AUTISM_KNOWLEDGE = {
    "what is autism": "Autism Spectrum Disorder (ASD) is a developmental condition that affects communication, behavior, and social interaction. Each person with autism is unique with their own strengths and challenges.",
    "signs of autism": "Common early signs include: delayed speech, avoiding eye contact, not responding to name, repetitive movements, sensory sensitivities, and difficulty with social interactions.",
    "aba therapy": "ABA (Applied Behavior Analysis) uses positive reinforcement to teach new skills and reduce challenging behaviors. It's evidence-based and considered the gold standard.",
    "speech therapy": "Speech therapy helps with communication skills, including verbal and non-verbal communication, articulation, and social language.",
    "occupational therapy": "Occupational therapy (OT) helps with sensory processing, fine motor skills, daily living skills, and self-regulation.",
    "how to handle meltdown": "Stay calm. Reduce sensory input. Ensure safety. Don't argue or punish. Give space and time to recover.",
    "sensory overload": "Signs include covering ears, hiding, crying, aggression. Help by reducing stimuli, moving to a quiet space, offering deep pressure.",
    "routine importance": "Routines provide predictability and reduce anxiety. Use visual schedules. Warn before transitions. Keep consistent daily patterns.",
    "how to communicate": "Use simple, clear language. Give extra time to process. Use visual supports. Be patient and listen actively.",
    "early intervention": "Early intervention (before age 3) greatly improves outcomes. Seek evaluation if concerned.",
    "pecs": "PECS (Picture Exchange Communication System) uses pictures to help non-verbal children communicate.",
    "visual schedule": "Visual schedules use pictures or words to show what will happen. They help with transitions and reduce anxiety.",
    "parent support": "Take care of yourself too! Join support groups, seek respite care, connect with other parents.",
    "school preparation": "Visit the school beforehand. Create a one-page profile about your child. Meet with teachers.",
    "social stories": "Social stories are short descriptions of social situations. They help children understand what to expect.",
    "stimming": "Stimming (repetitive movements) helps with self-regulation. It's not harmful unless it causes injury.",
    "eye contact": "Don't force eye contact. It can be uncomfortable. Use alternative ways to show attention."
}

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

# ==================== HTML Templates ====================
LANDING_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASD Support System - Pepper Robot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            text-align: center;
            padding: 40px;
        }
        h1 {
            font-size: 3em;
            color: white;
            margin-bottom: 20px;
        }
        .subtitle {
            color: #ccc;
            margin-bottom: 40px;
        }
        .buttons {
            display: flex;
            gap: 30px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            padding: 20px 50px;
            font-size: 1.5em;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: transform 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        .btn-parent {
            background: #e94560;
            color: white;
        }
        .btn-child {
            background: #0f3460;
            color: white;
        }
        .btn:hover {
            transform: scale(1.05);
        }
        .footer {
            margin-top: 50px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧩 ASD Support System</h1>
        <div class="subtitle">Pepper Robot - Integrated Support for Autism</div>
        <div class="buttons">
            <a href="/parent/login" class="btn btn-parent">👨‍👩‍👧 Parent Dashboard</a>
            <a href="/child/login" class="btn btn-child">🧒 Child Dashboard</a>
        </div>
        <div class="footer">ABA | TEACCH | PECS | Sensory Support | Educational Games</div>
    </div>
</body>
</html>
'''

PARENT_LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Parent Login - ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
            text-align: center;
        }
        h2 { color: #e94560; margin-bottom: 20px; }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #e94560;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin-top: 10px;
        }
        .link {
            margin-top: 15px;
            display: block;
            color: #ccc;
            text-decoration: none;
        }
        .error { color: #e94560; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>👨‍👩‍👧 Parent Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <a href="/parent/register" class="link">Don't have an account? Register</a>
        <a href="/" class="link">← Back</a>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

PARENT_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Parent Register - ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
            text-align: center;
        }
        h2 { color: #e94560; margin-bottom: 20px; }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #e94560;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin-top: 10px;
        }
        .link {
            margin-top: 15px;
            display: block;
            color: #ccc;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>📝 Parent Registration</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="email" name="email" placeholder="Email (optional)">
            <button type="submit">Register</button>
        </form>
        <a href="/parent/login" class="link">← Back to Login</a>
    </div>
</body>
</html>
'''

CHILD_LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Child Login - ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
            text-align: center;
        }
        h2 { color: #e94560; margin-bottom: 20px; }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #0f3460;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin-top: 10px;
        }
        .link {
            margin-top: 15px;
            display: block;
            color: #ccc;
            text-decoration: none;
        }
        .error { color: #e94560; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🧒 Child Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Child Name" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Enter</button>
        </form>
        <a href="/child/register" class="link">New child? Register</a>
        <a href="/" class="link">← Back</a>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

CHILD_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Child Register - ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
            text-align: center;
        }
        h2 { color: #e94560; margin-bottom: 20px; }
        input, select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        option { background: #1a1a2e; }
        button {
            width: 100%;
            padding: 12px;
            background: #e94560;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin-top: 10px;
        }
        .link {
            margin-top: 15px;
            display: block;
            color: #ccc;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>📝 New Child Registration</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Child Name" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="number" name="age" placeholder="Age" required>
            <select name="parent">
                <option value="">Select Parent</option>
                {% for parent in parents %}
                <option value="{{ parent }}">{{ parent }}</option>
                {% endfor %}
            </select>
            <button type="submit">Register</button>
        </form>
        <a href="/child/login" class="link">← Back to Login</a>
    </div>
</body>
</html>
'''

PARENT_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Parent Dashboard - ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(135deg, #0f3460, #1a1a2e);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .header h1 { color: #e94560; }
        .logout-btn {
            background: #e94560;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            color: white;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card h2 {
            color: #e94560;
            margin-bottom: 15px;
        }
        .child-selector {
            margin-bottom: 20px;
        }
        .child-btn {
            background: #0f3460;
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px;
            cursor: pointer;
            display: inline-block;
        }
        .child-btn.active {
            background: #e94560;
        }
        .stat {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #e94560;
        }
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
            max-height: 250px;
            overflow-y: auto;
        }
        .game-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 8px;
            text-align: center;
            font-size: 12px;
        }
        .chat-area {
            height: 200px;
            overflow-y: auto;
            margin-bottom: 10px;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        .message {
            margin: 5px 0;
            padding: 8px;
            border-radius: 10px;
            max-width: 85%;
        }
        .user-message {
            background: #e94560;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background: #0f3460;
        }
        .chat-input {
            display: flex;
            gap: 10px;
        }
        .chat-input input {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        .chat-input button {
            padding: 10px 20px;
            background: #e94560;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
        }
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .quick-btn {
            background: #0f3460;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 11px;
            cursor: pointer;
        }
        .routine-list li {
            padding: 8px;
            margin: 5px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
        }
        .routine-list li.completed {
            text-decoration: line-through;
            opacity: 0.6;
        }
        @media (max-width: 768px) {
            .dashboard { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>👨‍👩‍👧 Parent Dashboard</h1>
        <div>
            <span>Welcome, {{ username }}! </span>
            <a href="/parent/add_child" class="logout-btn" style="margin-right: 10px;">➕ Add Child</a>
            <a href="/parent/logout" class="logout-btn">Logout</a>
        </div>
    </div>
    
    <div class="dashboard">
        <!-- Child Selector -->
        <div class="card">
            <h2>👧 Select Child</h2>
            <div class="child-selector" id="childSelector">
                {% for child in children %}
                <div class="child-btn" onclick="selectChild('{{ child }}')">{{ child }}</div>
                {% endfor %}
            </div>
            {% if not children %}
            <p>No children added yet. Click "Add Child" to register your child.</p>
            {% endif %}
        </div>
        
        <!-- Progress Stats -->
        <div class="card" id="progressCard" style="display: none;">
            <h2>📊 Progress Report</h2>
            <div id="progressStats"></div>
        </div>
        
        <!-- Games Played -->
        <div class="card" id="gamesCard" style="display: none;">
            <h2>🎮 Games Played</h2>
            <div id="gamesList" class="games-grid"></div>
        </div>
        
        <!-- Autism Support Chatbot -->
        <div class="card">
            <h2>💬 Autism Support Chatbot</h2>
            <div class="chat-area" id="chatArea">
                <div class="message bot-message">Hello! I'm your Autism Support Assistant. Ask me anything about autism, therapies, communication, sensory needs, or daily routines.</div>
            </div>
            <div class="chat-input">
                <input type="text" id="chatInput" placeholder="Ask about autism..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Send</button>
            </div>
            <div class="quick-actions">
                <div class="quick-btn" onclick="quickQuestion('what is autism')">What is Autism?</div>
                <div class="quick-btn" onclick="quickQuestion('signs of autism')">Signs of Autism</div>
                <div class="quick-btn" onclick="quickQuestion('how to handle meltdown')">Meltdown Help</div>
                <div class="quick-btn" onclick="quickQuestion('aba therapy')">ABA Therapy</div>
                <div class="quick-btn" onclick="quickQuestion('sensory overload')">Sensory Overload</div>
                <div class="quick-btn" onclick="quickQuestion('routine importance')">Routine Tips</div>
            </div>
        </div>
    </div>
    
    <script>
        const children = {{ children | tojson }};
        let currentChild = null;
        
        function selectChild(childName) {
            currentChild = childName;
            document.querySelectorAll('.child-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            fetch(`/parent/child_progress/${childName}`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById('progressCard').style.display = 'block';
                    document.getElementById('gamesCard').style.display = 'block';
                    
                    // Progress stats
                    let statsHtml = `
                        <div class="stat"><span>🎯 Attention Score:</span><span class="stat-value">${data.attention || 75}%</span></div>
                        <div class="stat"><span>🎮 Games Played:</span><span class="stat-value">${data.games_played || 0}</span></div>
                        <div class="stat"><span>⭐ Total Points:</span><span class="stat-value">${data.total_points || 0}</span></div>
                        <div class="stat"><span>✅ Tasks Completed:</span><span class="stat-value">${data.tasks_completed || 0}</span></div>
                        <div class="stat"><span>🧘 Breathing Exercises:</span><span class="stat-value">${data.breathing_count || 0}</span></div>
                    `;
                    document.getElementById('progressStats').innerHTML = statsHtml;
                    
                    // Games list
                    let gamesHtml = '';
                    if (data.games) {
                        for (let [game, score] of Object.entries(data.games)) {
                            gamesHtml += `<div class="game-card"><div>${game.replace(/_/g, ' ')}</div><div style="color:#e94560;">⭐ ${score}</div></div>`;
                        }
                    }
                    if (gamesHtml === '') gamesHtml = '<p>No games played yet.</p>';
                    document.getElementById('gamesList').innerHTML = gamesHtml;
                });
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            input.value = '';
            
            fetch('/parent/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: message})
            })
            .then(res => res.json())
            .then(data => {
                setTimeout(() => addMessage(data.response, 'bot'), 300);
            });
        }
        
        function quickQuestion(q) {
            document.getElementById('chatInput').value = q;
            sendMessage();
        }
        
        function addMessage(text, sender) {
            const chatArea = document.getElementById('chatArea');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender === 'user' ? 'user-message' : 'bot-message'}`;
            msgDiv.innerHTML = text;
            chatArea.appendChild(msgDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        // Auto-select first child if exists
        if (children.length > 0) {
            setTimeout(() => {
                const firstBtn = document.querySelector('.child-btn');
                if (firstBtn) firstBtn.click();
            }, 100);
        }
    </script>
</body>
</html>
'''

CHILD_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Child Dashboard - ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(135deg, #0f3460, #1a1a2e);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .header h1 { color: #e94560; }
        .logout-btn {
            background: #e94560;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            color: white;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card h2 {
            color: #e94560;
            margin-bottom: 15px;
        }
        .breathing-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4a90e2, #357abd);
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            animation: breathe 4s ease-in-out infinite;
        }
        @keyframes breathe {
            0%, 100% { transform: scale(1); background: #4a90e2; }
            50% { transform: scale(1.2); background: #2c5f8a; }
        }
        .breathing-text { text-align: center; margin-top: 10px; }
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
            max-height: 300px;
            overflow-y: auto;
        }
        .game-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .game-card:hover {
            background: #e94560;
            transform: scale(1.05);
        }
        .routine-list li {
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
        }
        .routine-list li.completed {
            text-decoration: line-through;
            opacity: 0.6;
            background: rgba(76,175,80,0.3);
        }
        .stat {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            margin-top: 10px;
        }
        .stat-value { font-size: 24px; font-weight: bold; color: #e94560; }
        @media (max-width: 768px) {
            .dashboard { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧒 Welcome, {{ username }}!</h1>
        <a href="/child/logout" class="logout-btn">Logout</a>
    </div>
    
    <div class="dashboard">
        <!-- Breathing Exercise -->
        <div class="card">
            <h2>🧘 Calm Down - Breathing Exercise</h2>
            <div class="breathing-circle" id="breathingCircle" onclick="startBreathing()">
                <span style="text-align: center;">🧘<br>Breathe</span>
            </div>
            <div class="breathing-text" id="breathingText">Click the circle to start breathing exercise</div>
        </div>
        
        <!-- Daily Routine -->
        <div class="card">
            <h2>📋 My Daily Tasks</h2>
            <ul class="routine-list" id="routineList"></ul>
            <div class="stat">
                <span>✅ Completed today:</span>
                <span class="stat-value" id="taskCount">0</span>
            </div>
        </div>
        
        <!-- Educational Games -->
        <div class="card">
            <h2>🎮 My Games</h2>
            <div class="games-grid" id="gamesGrid"></div>
        </div>
    </div>
    
    <script>
        const games = {{ games | tojson }};
        const icons = {{ icons | tojson }};
        
        const routines = {
            morning: ["Wake up 🛌", "Brush teeth 🪥", "Wash face 🧼", "Get dressed 👕", "Eat breakfast 🍳"],
            afternoon: ["Learning time 📚", "Play time 🎮", "Eat lunch 🍎", "Rest time 😴"],
            evening: ["Eat dinner 🍽️", "Bath time 🛁", "Read story 📖", "Brush teeth 🪥", "Bedtime 😴"]
        };
        
        let currentRoutine = "morning";
        let completedTasks = localStorage.getItem("child_completedTasks") ? JSON.parse(localStorage.getItem("child_completedTasks")) : [];
        
        function updateRoutineList() {
            const list = document.getElementById("routineList");
            list.innerHTML = "";
            routines[currentRoutine].forEach(task => {
                const li = document.createElement("li");
                li.innerHTML = `<span>${task}</span><span>✅</span>`;
                if (completedTasks.includes(task)) {
                    li.classList.add("completed");
                }
                li.onclick = () => toggleTask(li, task);
                list.appendChild(li);
            });
            document.getElementById("taskCount").innerText = completedTasks.length;
        }
        
        function toggleTask(element, task) {
            if (element.classList.contains("completed")) {
                element.classList.remove("completed");
                completedTasks = completedTasks.filter(t => t !== task);
            } else {
                element.classList.add("completed");
                completedTasks.push(task);
            }
            localStorage.setItem("child_completedTasks", JSON.stringify(completedTasks));
            document.getElementById("taskCount").innerText = completedTasks.length;
        }
        
        let breathingInterval;
        function startBreathing() {
            const textDiv = document.getElementById("breathingText");
            let step = 0;
            const phases = ["Breathe in... 4 seconds", "Hold... 4 seconds", "Breathe out... 4 seconds"];
            
            if (breathingInterval) clearInterval(breathingInterval);
            
            breathingInterval = setInterval(() => {
                textDiv.innerHTML = phases[step % 3];
                step++;
                if (step >= 9) {
                    clearInterval(breathingInterval);
                    textDiv.innerHTML = "✨ Great job! You're calm now! ✨";
                    setTimeout(() => {
                        textDiv.innerHTML = "Click the circle to start breathing exercise";
                    }, 3000);
                }
            }, 4000);
        }
        
        function loadGames() {
            const grid = document.getElementById("gamesGrid");
            grid.innerHTML = "";
            games.forEach(game => {
                const card = document.createElement("div");
                card.className = "game-card";
                card.innerHTML = `<div style="font-size: 32px;">${icons[game] || '🎮'}</div><div>${game.replace(/_/g, ' ')}</div>`;
                card.onclick = () => window.location.href = `/game/${game}`;
                grid.appendChild(card);
            });
        }
        
        updateRoutineList();
        loadGames();
    </script>
</body>
</html>
'''

ADD_CHILD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Add Child - ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
            text-align: center;
        }
        h2 { color: #e94560; margin-bottom: 20px; }
        input, select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        option { background: #1a1a2e; }
        button {
            width: 100%;
            padding: 12px;
            background: #e94560;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin-top: 10px;
        }
        .link {
            margin-top: 15px;
            display: block;
            color: #ccc;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>➕ Add New Child</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Child Name" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="number" name="age" placeholder="Age" required>
            <button type="submit">Add Child</button>
        </form>
        <a href="/parent/dashboard" class="link">← Back to Dashboard</a>
    </div>
</body>
</html>
'''

# ==================== Flask Routes ====================
@app.route('/')
def landing():
    return render_template_string(LANDING_TEMPLATE)

# Parent Routes
@app.route('/parent/login', methods=['GET', 'POST'])
def parent_login():
    if request.method == 'POST':
        parents, _, _ = load_data()
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        
        if username in parents and parents[username]['password'] == password:
            session['parent'] = username
            return redirect(url_for('parent_dashboard'))
        return render_template_string(PARENT_LOGIN_TEMPLATE, error='Invalid credentials')
    return render_template_string(PARENT_LOGIN_TEMPLATE)

@app.route('/parent/register', methods=['GET', 'POST'])
def parent_register():
    if request.method == 'POST':
        parents, _, _ = load_data()
        username = request.form['username']
        
        if username in parents:
            return render_template_string(PARENT_REGISTER_TEMPLATE, error='Username exists')
        
        parents[username] = {
            'password': hashlib.md5(request.form['password'].encode()).hexdigest(),
            'email': request.form.get('email', ''),
            'children': []
        }
        save_data(parents, *load_data()[1:])
        return redirect(url_for('parent_login'))
    return render_template_string(PARENT_REGISTER_TEMPLATE)

@app.route('/parent/dashboard')
def parent_dashboard():
    if 'parent' not in session:
        return redirect(url_for('parent_login'))
    
    parents, children, _ = load_data()
    parent = session['parent']
    child_list = parents[parent].get('children', [])
    
    return render_template_string(PARENT_DASHBOARD_TEMPLATE, username=parent, children=child_list)

@app.route('/parent/add_child', methods=['GET', 'POST'])
def parent_add_child():
    if 'parent' not in session:
        return redirect(url_for('parent_login'))
    
    if request.method == 'POST':
        parents, children, progress = load_data()
        parent = session['parent']
        child_name = request.form['username']
        
        if child_name not in children:
            children[child_name] = {
                'password': hashlib.md5(request.form['password'].encode()).hexdigest(),
                'age': request.form['age'],
                'parent': parent
            }
            parents[parent]['children'].append(child_name)
            progress[child_name] = {
                'games': {g: 0 for g in GAMES_LIST},
                'total_points': 0,
                'games_played': 0,
                'attention': 75,
                'tasks_completed': 0,
                'breathing_count': 0
            }
            save_data(parents, children, progress)
        return redirect(url_for('parent_dashboard'))
    return render_template_string(ADD_CHILD_TEMPLATE)

@app.route('/parent/child_progress/<child_name>')
def child_progress(child_name):
    _, _, progress = load_data()
    child_data = progress.get(child_name, {})
    return jsonify({
        'attention': child_data.get('attention', 75),
        'games_played': child_data.get('games_played', 0),
        'total_points': child_data.get('total_points', 0),
        'tasks_completed': child_data.get('tasks_completed', 0),
        'breathing_count': child_data.get('breathing_count', 0),
        'games': child_data.get('games', {})
    })

@app.route('/parent/chat', methods=['POST'])
def parent_chat():
    data = request.json
    question = data.get('question', '').lower()
    
    for key, answer in AUTISM_KNOWLEDGE.items():
        if key in question:
            return jsonify({'response': answer})
    return jsonify({'response': "I'm here to help! Ask me about autism signs, therapies, communication, sensory needs, meltdowns, or routines."})

@app.route('/parent/logout')
def parent_logout():
    session.pop('parent', None)
    return redirect(url_for('landing'))

# Child Routes
@app.route('/child/login', methods=['GET', 'POST'])
def child_login():
    if request.method == 'POST':
        _, children, _ = load_data()
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        
        if username in children and children[username]['password'] == password:
            session['child'] = username
            return redirect(url_for('child_dashboard'))
        return render_template_string(CHILD_LOGIN_TEMPLATE, error='Invalid credentials')
    return render_template_string(CHILD_LOGIN_TEMPLATE)

@app.route('/child/register', methods=['GET', 'POST'])
def child_register():
    if request.method == 'POST':
        parents, children, progress = load_data()
        child_name = request.form['username']
        parent_name = request.form.get('parent')
        
        if child_name in children:
            return render_template_string(CHILD_REGISTER_TEMPLATE, parents=list(parents.keys()), error='Child exists')
        
        children[child_name] = {
            'password': hashlib.md5(request.form['password'].encode()).hexdigest(),
            'age': request.form['age'],
            'parent': parent_name
        }
        if parent_name and parent_name in parents:
            parents[parent_name]['children'].append(child_name)
        
        progress[child_name] = {
            'games': {g: 0 for g in GAMES_LIST},
            'total_points': 0,
            'games_played': 0,
            'attention': 75,
            'tasks_completed': 0,
            'breathing_count': 0
        }
        save_data(parents, children, progress)
        return redirect(url_for('child_login'))
    
    parents, _, _ = load_data()
    return render_template_string(CHILD_REGISTER_TEMPLATE, parents=list(parents.keys()))

@app.route('/child/dashboard')
def child_dashboard():
    if 'child' not in session:
        return redirect(url_for('child_login'))
    return render_template_string(CHILD_DASHBOARD_TEMPLATE, username=session['child'], games=GAMES_LIST, icons=ICONS)

@app.route('/child/logout')
def child_logout():
    session.pop('child', None)
    return redirect(url_for('landing'))

@app.route('/game/<game_name>')
def play_game(game_name):
    return render_template(f'games/{game_name}.html')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧩 ASD COMPLETE DASHBOARD")
    print("="*50)
    print("👨‍👩‍👧 Parent Dashboard - مراقبة التقدم")
    print("🧒 Child Dashboard - ألعاب + تمارين")
    print("💬 Autism Support Chatbot")
    print(f"🎮 Games available: {len(GAMES_LIST)}")
    print("="*50)
    print("🌐 Opening at: http://localhost:5001")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
