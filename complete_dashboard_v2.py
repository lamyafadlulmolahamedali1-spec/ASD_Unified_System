#!/usr/bin/env python3
"""
ASD Complete Dashboard V2
- Parents Dashboard: Graphs, ABA Analysis, DTT, TEACCH, Emotion Tracking
- Child Dashboard: Games + ABA-based AI Chat
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
import random
import hashlib
import math
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'asd_secret_key_2024'

DATA_DIR = '/home/lamya/Desktop/ASD_Complete_Project_20260325_161142/data'
os.makedirs(DATA_DIR, exist_ok=True)

# ==================== ABA, DTT, TEACCH Data ====================
def generate_mock_data():
    """توليد بيانات افتراضية للرسوم البيانية"""
    dates = [(datetime.now() - timedelta(days=i)).strftime('%m/%d') for i in range(7, -1, -1)]
    attention_data = [random.randint(60, 95) for _ in range(8)]
    emotion_data = [random.choice(['happy', 'neutral', 'sad', 'excited']) for _ in range(8)]
    aba_scores = [random.randint(50, 100) for _ in range(8)]
    dtt_scores = [random.randint(40, 95) for _ in range(8)]
    teacch_scores = [random.randint(55, 98) for _ in range(8)]
    
    emotion_counts = {'happy': 0, 'neutral': 0, 'sad': 0, 'excited': 0}
    for e in emotion_data:
        emotion_counts[e] += 1
    
    return {
        'dates': dates,
        'attention': attention_data,
        'emotion': emotion_data,
        'emotion_counts': emotion_counts,
        'aba': aba_scores,
        'dtt': dtt_scores,
        'teacch': teacch_scores
    }

# ==================== Autism Knowledge Base (Extended) ====================
AUTISM_KNOWLEDGE = {
    "what is autism": "Autism Spectrum Disorder (ASD) is a developmental condition that affects communication, behavior, and social interaction. Each person with autism is unique with their own strengths and challenges.",
    "signs of autism": "Common early signs include: delayed speech, avoiding eye contact, not responding to name, repetitive movements, sensory sensitivities, and difficulty with social interactions.",
    "aba therapy": "ABA (Applied Behavior Analysis) uses positive reinforcement to teach new skills and reduce challenging behaviors. It's evidence-based and considered the gold standard.",
    "dtt therapy": "DTT (Discrete Trial Training) breaks skills into small steps. Each trial has an instruction, response, and consequence. It's very effective for teaching new skills.",
    "teacch": "TEACCH uses visual schedules and structured environments. It emphasizes visual learning and predictable routines.",
    "how to handle meltdown": "Stay calm. Reduce sensory input. Ensure safety. Don't argue or punish. Give space and time to recover.",
    "sensory overload": "Signs include covering ears, hiding, crying, aggression. Help by reducing stimuli, moving to a quiet space, offering deep pressure.",
    "positive reinforcement": "Praise specific behaviors. Use rewards immediately. Be consistent. Focus on what the child did well.",
    "prompting": "Use least-to-most prompting. Start with verbal, then gesture, then model, then physical. Fade prompts quickly.",
    "task analysis": "Break complex tasks into small steps. Teach one step at a time. Chain steps together gradually."
}

# ==================== ABA-Based AI Prompt ====================
ABA_THERAPY_PROMPT = """You are Pepper, a friendly robot assistant for a child with autism. 
Use these therapy methods:

ABA (Applied Behavior Analysis):
- Give positive reinforcement: "Great job!", "Excellent!", "You did it!"
- Use clear, simple instructions
- Praise every attempt
- Break tasks into small steps

DTT (Discrete Trial Training):
- Give one instruction at a time
- Wait for response
- Provide immediate feedback
- Keep trials short and successful

TEACCH:
- Use structured responses
- Be predictable
- Use visual language
- Follow routines

Rules:
- Respond in 1 short, fun sentence
- Be excited and encouraging
- Use emojis 😊
- Always reinforce positively
- Keep language simple

Child's message: {message}
Respond with an encouraging, therapeutic message:"""

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
        h1 { font-size: 3em; color: white; margin-bottom: 20px; }
        .subtitle { color: #ccc; margin-bottom: 40px; }
        .buttons { display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; }
        .btn {
            padding: 20px 50px;
            font-size: 1.5em;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .btn-parent { background: #e94560; color: white; }
        .btn-child { background: #0f3460; color: white; }
        .btn:hover { transform: scale(1.05); }
        .footer { margin-top: 50px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧩 ASD Support System</h1>
        <div class="subtitle">Pepper Robot - ABA | DTT | TEACCH | Integrated Support</div>
        <div class="buttons">
            <a href="/parent/login" class="btn btn-parent">👨‍👩‍👧 Parent Dashboard</a>
            <a href="/child/login" class="btn btn-child">🧒 Child Dashboard</a>
        </div>
        <div class="footer">ABA Therapy | DTT | TEACCH | Emotion Tracking | Educational Games</div>
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
        }
        .link { margin-top: 15px; display: block; color: #ccc; text-decoration: none; }
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
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
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
        }
        .link { margin-top: 15px; display: block; color: #ccc; text-decoration: none; }
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
        }
        .link { margin-top: 15px; display: block; color: #ccc; text-decoration: none; }
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
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
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
        }
        .link { margin-top: 15px; display: block; color: #ccc; text-decoration: none; }
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
        }
        .link { margin-top: 15px; display: block; color: #ccc; text-decoration: none; }
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

PARENT_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Parent Dashboard - ASD Support</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
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
        .card h2 { color: #e94560; margin-bottom: 15px; }
        .child-selector { margin-bottom: 20px; }
        .child-btn {
            background: #0f3460;
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px;
            cursor: pointer;
            display: inline-block;
        }
        .child-btn.active { background: #e94560; }
        .stat {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        .stat-value { font-size: 24px; font-weight: bold; color: #e94560; }
        canvas { max-height: 200px; margin: 10px 0; }
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 8px;
            max-height: 200px;
            overflow-y: auto;
        }
        .game-card {
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 5px;
            text-align: center;
            font-size: 10px;
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
        @media (max-width: 768px) { .dashboard { grid-template-columns: 1fr; } }
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
        <div class="card">
            <h2>👧 Select Child</h2>
            <div class="child-selector" id="childSelector">
                {% for child in children %}
                <div class="child-btn" onclick="selectChild('{{ child }}')">{{ child }}</div>
                {% endfor %}
            </div>
        </div>
        
        <div class="card" id="progressCard" style="display: none;">
            <h2>📊 Progress Overview</h2>
            <div id="progressStats"></div>
        </div>
        
        <div class="card" id="attentionChartCard" style="display: none;">
            <h2>📈 Attention & Focus Trend</h2>
            <canvas id="attentionChart"></canvas>
        </div>
        
        <div class="card" id="abaChartCard" style="display: none;">
            <h2>📊 ABA | DTT | TEACCH Progress</h2>
            <canvas id="therapyChart"></canvas>
        </div>
        
        <div class="card" id="emotionCard" style="display: none;">
            <h2>😊 Emotion Analysis</h2>
            <canvas id="emotionChart"></canvas>
        </div>
        
        <div class="card" id="gamesCard" style="display: none;">
            <h2>🎮 Games Played</h2>
            <div id="gamesList" class="games-grid"></div>
        </div>
        
        <div class="card" id="teacchCard" style="display: none;">
            <h2>📋 TEACCH Daily Tasks</h2>
            <ul class="routine-list" id="teacchList"></ul>
        </div>
    </div>
    
    <script>
        let currentChild = null;
        let attentionChart, therapyChart, emotionChart;
        
        function selectChild(childName) {
            currentChild = childName;
            document.querySelectorAll('.child-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            fetch(`/parent/child_progress/${childName}`)
                .then(res => res.json())
                .then(data => {
                    document.querySelectorAll('#progressCard, #attentionChartCard, #abaChartCard, #emotionCard, #gamesCard, #teacchCard').forEach(c => c.style.display = 'block');
                    
                    // Progress stats
                    document.getElementById('progressStats').innerHTML = `
                        <div class="stat"><span>🎯 Attention Score:</span><span class="stat-value">${data.attention}%</span></div>
                        <div class="stat"><span>🎮 Games Played:</span><span class="stat-value">${data.games_played}</span></div>
                        <div class="stat"><span>⭐ Total Points:</span><span class="stat-value">${data.total_points}</span></div>
                        <div class="stat"><span>✅ Tasks Completed:</span><span class="stat-value">${data.tasks_completed}</span></div>
                        <div class="stat"><span>🧘 Breathing Exercises:</span><span class="stat-value">${data.breathing_count}</span></div>
                    `;
                    
                    // Attention Chart
                    if (attentionChart) attentionChart.destroy();
                    const attentionCtx = document.getElementById('attentionChart').getContext('2d');
                    attentionChart = new Chart(attentionCtx, {
                        type: 'line',
                        data: { labels: data.dates, datasets: [{ label: 'Attention %', data: data.attention_data, borderColor: '#e94560', fill: false, tension: 0.3 }] },
                        options: { responsive: true, maintainAspectRatio: true }
                    });
                    
                    // Therapy Chart
                    if (therapyChart) therapyChart.destroy();
                    const therapyCtx = document.getElementById('therapyChart').getContext('2d');
                    therapyChart = new Chart(therapyCtx, {
                        type: 'line',
                        data: { labels: data.dates, datasets: [
                            { label: 'ABA', data: data.aba_data, borderColor: '#4a90e2', fill: false },
                            { label: 'DTT', data: data.dtt_data, borderColor: '#e94560', fill: false },
                            { label: 'TEACCH', data: data.teacch_data, borderColor: '#4caf50', fill: false }
                        ] },
                        options: { responsive: true, maintainAspectRatio: true }
                    });
                    
                    // Emotion Chart
                    if (emotionChart) emotionChart.destroy();
                    const emotionCtx = document.getElementById('emotionChart').getContext('2d');
                    emotionChart = new Chart(emotionCtx, {
                        type: 'pie',
                        data: { labels: ['Happy', 'Neutral', 'Sad', 'Excited'], datasets: [{ data: [data.emotion_counts.happy, data.emotion_counts.neutral, data.emotion_counts.sad, data.emotion_counts.excited], backgroundColor: ['#4caf50', '#9e9e9e', '#f44336', '#ff9800'] }] },
                        options: { responsive: true, maintainAspectRatio: true }
                    });
                    
                    // Games list
                    let gamesHtml = '';
                    for (let [game, score] of Object.entries(data.games)) {
                        if (score > 0) gamesHtml += `<div class="game-card"><div>${game.replace(/_/g, ' ')}</div><div style="color:#e94560;">⭐ ${score}</div></div>`;
                    }
                    document.getElementById('gamesList').innerHTML = gamesHtml || '<p>No games played yet.</p>';
                    
                    // TEACCH Tasks
                    let tasksHtml = '';
                    const tasks = ['Morning Routine', 'Complete Learning Activity', 'Play Educational Game', 'Practice Communication', 'Follow Visual Schedule'];
                    tasks.forEach(task => { tasksHtml += `<li onclick="toggleTeacch(this)"><span>${task}</span><span>✅</span></li>`; });
                    document.getElementById('teacchList').innerHTML = tasksHtml;
                });
        }
        
        function toggleTeacch(element) {
            element.classList.toggle('completed');
        }
        
        // Auto-select first child
        setTimeout(() => { const firstBtn = document.querySelector('.child-btn'); if (firstBtn) firstBtn.click(); }, 100);
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
            max-width: 1400px;
            margin: 0 auto;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card h2 { color: #e94560; margin-bottom: 15px; }
        .chat-area {
            height: 250px;
            overflow-y: auto;
            margin-bottom: 10px;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        .message {
            margin: 8px 0;
            padding: 8px;
            border-radius: 10px;
            max-width: 85%;
        }
        .user-message { background: #e94560; margin-left: auto; text-align: right; }
        .bot-message { background: #0f3460; }
        .chat-input { display: flex; gap: 10px; margin-top: 10px; }
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
        .quick-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
        .quick-btn {
            background: #0f3460;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 11px;
            cursor: pointer;
        }
        .breathing-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4a90e2, #357abd);
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            animation: breathe 4s ease-in-out infinite;
        }
        @keyframes breathe { 0%,100% { transform: scale(1); } 50% { transform: scale(1.15); } }
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
            padding: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .game-card:hover { background: #e94560; transform: scale(1.05); }
        .routine-list li {
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
        }
        .routine-list li.completed { text-decoration: line-through; opacity: 0.6; }
        @media (max-width: 768px) { .dashboard { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧒 Welcome, {{ username }}!</h1>
        <a href="/child/logout" class="logout-btn">Logout</a>
    </div>
    
    <div class="dashboard">
        <div class="card">
            <h2>💬 Pepper - Your Therapy Friend</h2>
            <div class="chat-area" id="chatArea">
                <div class="message bot-message">Hi {{ username }}! I'm Pepper! 😊 I'm here to help you learn and have fun! What would you like to talk about or play today? 🌟</div>
            </div>
            <div class="chat-input">
                <input type="text" id="chatInput" placeholder="Type your message..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Send</button>
            </div>
            <div class="quick-actions">
                <div class="quick-btn" onclick="quickMessage('I did something good today!')">🎉 Good Job</div>
                <div class="quick-btn" onclick="quickMessage('I feel happy')">😊 Happy</div>
                <div class="quick-btn" onclick="quickMessage('I need a break')">😌 Break</div>
                <div class="quick-btn" onclick="quickMessage('Help me with this')">🆘 Help</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🧘 Calm Down - Breathing</h2>
            <div class="breathing-circle" onclick="startBreathing()"><span>🧘<br>Breathe</span></div>
            <div id="breathingText" style="text-align: center;">Click to start</div>
        </div>
        
        <div class="card">
            <h2>📋 My Daily Tasks (TEACCH)</h2>
            <ul class="routine-list" id="routineList"></ul>
        </div>
        
        <div class="card">
            <h2>🎮 My Games</h2>
            <div class="games-grid" id="gamesGrid"></div>
        </div>
    </div>
    
    <script>
        const games = {{ games | tojson }};
        const icons = {{ icons | tojson }};
        const tasks = ["Wake up & get ready 🛌", "Complete learning activity 📚", "Play a game 🎮", "Practice communication 💬", "Follow visual schedule 📋"];
        let completedTasks = JSON.parse(localStorage.getItem('child_tasks') || '[]');
        
        function loadTasks() {
            const list = document.getElementById('routineList');
            list.innerHTML = '';
            tasks.forEach(task => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${task}</span><span>✅</span>`;
                if (completedTasks.includes(task)) li.classList.add('completed');
                li.onclick = () => {
                    if (li.classList.contains('completed')) {
                        li.classList.remove('completed');
                        completedTasks = completedTasks.filter(t => t !== task);
                    } else {
                        li.classList.add('completed');
                        completedTasks.push(task);
                    }
                    localStorage.setItem('child_tasks', JSON.stringify(completedTasks));
                };
                list.appendChild(li);
            });
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const msg = input.value.trim();
            if (!msg) return;
            
            addMessage(msg, 'user');
            input.value = '';
            
            fetch('/child/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            })
            .then(res => res.json())
            .then(data => setTimeout(() => addMessage(data.response, 'bot'), 300));
        }
        
        function quickMessage(msg) {
            document.getElementById('chatInput').value = msg;
            sendMessage();
        }
        
        function addMessage(text, sender) {
            const area = document.getElementById('chatArea');
            const div = document.createElement('div');
            div.className = `message ${sender === 'user' ? 'user-message' : 'bot-message'}`;
            div.innerHTML = text;
            area.appendChild(div);
            area.scrollTop = area.scrollHeight;
        }
        
        let breathingInterval;
        function startBreathing() {
            const textDiv = document.getElementById('breathingText');
            let step = 0;
            const phases = ["Breathe in... 4 seconds", "Hold... 4 seconds", "Breathe out... 4 seconds"];
            if (breathingInterval) clearInterval(breathingInterval);
            breathingInterval = setInterval(() => {
                textDiv.innerHTML = phases[step % 3];
                step++;
                if (step >= 9) {
                    clearInterval(breathingInterval);
                    textDiv.innerHTML = "✨ Great job! ✨";
                    setTimeout(() => textDiv.innerHTML = "Click to start", 2000);
                }
            }, 4000);
        }
        
        function loadGames() {
            const grid = document.getElementById('gamesGrid');
            grid.innerHTML = '';
            games.forEach(game => {
                const card = document.createElement('div');
                card.className = 'game-card';
                card.innerHTML = `<div style="font-size: 32px;">${icons[game] || '🎮'}</div><div>${game.replace(/_/g, ' ')}</div>`;
                card.onclick = () => window.location.href = `/game/${game}`;
                grid.appendChild(card);
            });
        }
        
        loadTasks();
        loadGames();
    </script>
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
        parents[username] = {'password': hashlib.md5(request.form['password'].encode()).hexdigest(), 'email': request.form.get('email', ''), 'children': []}
        save_data(parents, *load_data()[1:])
        return redirect(url_for('parent_login'))
    return render_template_string(PARENT_REGISTER_TEMPLATE)

@app.route('/parent/dashboard')
def parent_dashboard():
    if 'parent' not in session:
        return redirect(url_for('parent_login'))
    parents, _, _ = load_data()
    return render_template_string(PARENT_DASHBOARD_TEMPLATE, username=session['parent'], children=parents[session['parent']].get('children', []))

@app.route('/parent/add_child', methods=['GET', 'POST'])
def parent_add_child():
    if 'parent' not in session:
        return redirect(url_for('parent_login'))
    if request.method == 'POST':
        parents, children, progress = load_data()
        parent = session['parent']
        child_name = request.form['username']
        if child_name not in children:
            children[child_name] = {'password': hashlib.md5(request.form['password'].encode()).hexdigest(), 'age': request.form['age'], 'parent': parent}
            parents[parent]['children'].append(child_name)
            progress[child_name] = {'games': {g: 0 for g in GAMES_LIST}, 'total_points': 0, 'games_played': 0, 'attention': 75, 'tasks_completed': 0, 'breathing_count': 0}
            save_data(parents, children, progress)
        return redirect(url_for('parent_dashboard'))
    return render_template_string(ADD_CHILD_TEMPLATE)

@app.route('/parent/child_progress/<child_name>')
def child_progress(child_name):
    _, _, progress = load_data()
    child_data = progress.get(child_name, {})
    mock = generate_mock_data()
    return jsonify({
        'attention': child_data.get('attention', 75),
        'games_played': child_data.get('games_played', 0),
        'total_points': child_data.get('total_points', 0),
        'tasks_completed': child_data.get('tasks_completed', 0),
        'breathing_count': child_data.get('breathing_count', 0),
        'games': child_data.get('games', {}),
        'dates': mock['dates'],
        'attention_data': mock['attention'],
        'aba_data': mock['aba'],
        'dtt_data': mock['dtt'],
        'teacch_data': mock['teacch'],
        'emotion_counts': mock['emotion_counts']
    })

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
            parents_list = list(parents.keys())
            return render_template_string(CHILD_REGISTER_TEMPLATE, parents=parents_list, error='Child exists')
        children[child_name] = {'password': hashlib.md5(request.form['password'].encode()).hexdigest(), 'age': request.form['age'], 'parent': parent_name}
        if parent_name and parent_name in parents:
            parents[parent_name]['children'].append(child_name)
        progress[child_name] = {'games': {g: 0 for g in GAMES_LIST}, 'total_points': 0, 'games_played': 0, 'attention': 75, 'tasks_completed': 0, 'breathing_count': 0}
        save_data(parents, children, progress)
        return redirect(url_for('child_login'))
    parents, _, _ = load_data()
    return render_template_string(CHILD_REGISTER_TEMPLATE, parents=list(parents.keys()))

@app.route('/child/dashboard')
def child_dashboard():
    if 'child' not in session:
        return redirect(url_for('child_login'))
    return render_template_string(CHILD_DASHBOARD_TEMPLATE, username=session['child'], games=GAMES_LIST, icons=ICONS)

@app.route('/child/chat', methods=['POST'])
def child_chat():
    data = request.json
    message = data.get('message', '')
    
    # Simple ABA-based responses (can be expanded with real AI)
    message_lower = message.lower()
    
    if 'good' in message_lower or 'great' in message_lower:
        response = "That's wonderful! 🌟 I'm so proud of you! Keep up the great work! 👏"
    elif 'sad' in message_lower or 'upset' in message_lower:
        response = "It's okay to feel sad sometimes. 🤗 I'm here with you. Let's take a deep breath together. 🧘"
    elif 'help' in message_lower:
        response = "I'm here to help you! 💪 What do you need assistance with? You can do this! 🌟"
    elif 'break' in message_lower:
        response = "Taking a break is a great idea! 😌 Let's do our breathing exercise to relax. 🧘"
    elif 'happy' in message_lower:
        response = "Yay! I'm so happy you're feeling happy! 😊 Your smile makes my day brighter! 🌟"
    elif 'game' in message_lower or 'play' in message_lower:
        response = "Great idea! Let's play a game! 🎮 Look at the 'My Games' section and choose one you like! 🌟"
    elif 'thank' in message_lower:
        response = "You're very welcome! 🤗 I love helping you learn and grow! 🌟"
    else:
        response = "That's interesting! 🎉 Tell me more! I love learning from you. What would you like to do next? 🌟"
    
    return jsonify({'response': response})

@app.route('/child/logout')
def child_logout():
    session.pop('child', None)
    return redirect(url_for('landing'))

@app.route('/game/<game_name>')
def play_game(game_name):
    return render_template(f'games/{game_name}.html')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧩 ASD COMPLETE DASHBOARD V2")
    print("="*50)
    print("✅ Parents Dashboard - Graphs, ABA, DTT, TEACCH, Emotion Tracking")
    print("✅ Child Dashboard - ABA-based AI Chat + Games")
    print(f"🎮 Games available: {len(GAMES_LIST)}")
    print("="*50)
    print("🌐 Opening at: http://localhost:5001")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
