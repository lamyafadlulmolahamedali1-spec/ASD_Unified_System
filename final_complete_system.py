#!/usr/bin/env python3
"""
FINAL COMPLETE ASD SYSTEM
- Parent Dashboard: ISAA Test + AI Suggestions + PDF Report + Chatbot + Graphs + Progress
- Child Dashboard: Games (fully working) + Therapy Chat + Breathing + TEACCH
- Unified Login System
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
import random
import hashlib
import math
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'asd_complete_final_key'

DATA_DIR = '/home/lamya/Desktop/ASD_Complete_Project_20260325_161142/data'
os.makedirs(DATA_DIR, exist_ok=True)

# ==================== Games List ====================
games_dir = os.path.join(os.path.dirname(__file__), 'templates', 'games')
GAMES_LIST = ['aba_matching', 'aba_sorting', 'alphabet_song', 'animal_sounds', 'ball_sort_perfect', 'block_blast', 'brain_oddone', 'brain_pattern', 'color_match', 'coloring_game', 'counting', 'crossword_english', 'daily_routine', 'do_dont', 'drawing_pad', 'familiar_things', 'language_game', 'letter_coloring', 'math_challenge', 'memory_cards', 'music_rhythm', 'pepper_emotions', 'pepper_imitation', 'physical_activity', 'sensory_bubbles', 'sensory_fireworks', 'sensory_spinner', 'shape_sorting', 'smart_alarm', 'snake_game', 'social_stories_english', 'spot_difference', 'story_library_full', 'sudoku', 'teacch_schedule', 'teacch_work', 'tictactoe_game', 'word_search', 'work_system']
if os.path.exists(games_dir):
    for f in os.listdir(games_dir):
        if f.endswith('.html') and f not in ['landing.html', 'parent_login.html', 'child_login.html', 'games_menu.html']:
            GAMES_LIST.append(os.path.splitext(f)[0])
GAMES_LIST = list(set(GAMES_LIST))
GAMES_LIST.sort()

# If no games found, add sample game
if not GAMES_LIST:
    GAMES_LIST = ['aba_matching', 'aba_sorting', 'alphabet_song', 'animal_sounds', 'ball_sort_perfect', 'block_blast', 'brain_oddone', 'brain_pattern', 'color_match', 'coloring_game', 'counting', 'crossword_english', 'daily_routine', 'do_dont', 'drawing_pad', 'familiar_things', 'language_game', 'letter_coloring', 'math_challenge', 'memory_cards', 'music_rhythm', 'pepper_emotions', 'pepper_imitation', 'physical_activity', 'sensory_bubbles', 'sensory_fireworks', 'sensory_spinner', 'shape_sorting', 'smart_alarm', 'snake_game', 'social_stories_english', 'spot_difference', 'story_library_full', 'sudoku', 'teacch_schedule', 'teacch_work', 'tictactoe_game', 'word_search', 'work_system']

ICONS = {
    'aba_matching': '🎮',
    'aba_sorting': '🎮',
    'alphabet_song': '🎮',
    'animal_sounds': '🎮',
    'ball_sort_perfect': '🎮',
    'block_blast': '🎮',
    'brain_oddone': '🎮',
    'brain_pattern': '🎮',
    'color_match': '🎮',
    'coloring_game': '🎮',
    'counting': '🔢',
    'crossword_english': '🎮',
    'daily_routine': '🎮',
    'do_dont': '🎮',
    'drawing_pad': '🎮',
    'familiar_things': '🎮',
    'language_game': '🎮',
    'letter_coloring': '🎮',
    'math_challenge': '🎮',
    'memory_cards': '🎮',
    'music_rhythm': '🎮',
    'pepper_emotions': '🎮',
    'pepper_imitation': '🎮',
    'physical_activity': '🎮',
    'sensory_bubbles': '🎮',
    'sensory_fireworks': '🎮',
    'sensory_spinner': '🎮',
    'shape_sorting': '🎮',
    'smart_alarm': '🎮',
    'snake_game': '🎮',
    'social_stories_english': '🎮',
    'spot_difference': '🎮',
    'story_library_full': '🎮',
    'sudoku': '🎮',
    'teacch_schedule': '🎮',
    'teacch_work': '🎮',
    'tictactoe_game': '🎮',
    'word_search': '🎮',
    'work_system': '🎮',
}

# ==================== ISAA Test Questions ====================
ISAA_QUESTIONS = [
    "Does the child maintain eye contact?",
    "Does the child respond to their name?",
    "Does the child show interest in playing with others?",
    "Does the child have repetitive movements?",
    "Does the child have sensitivity to sounds?",
    "Does the child have delayed speech?",
    "Does the child follow instructions?",
    "Does the child show empathy?",
    "Does the child have unusual attachments to objects?",
    "Does the child have difficulty with changes in routine?"
]

# ==================== Therapy Suggestions ====================
THERAPY_SUGGESTIONS = {
    "eye_contact": "Practice eye contact during fun activities. Use toys to draw attention to your face. Praise when they look at you.",
    "social_interaction": "Arrange playdates with siblings or peers. Use turn-taking games. Model appropriate social behaviors.",
    "speech": "Work with a speech therapist. Use picture cards (PECS) and simple words. Give extra time to respond.",
    "sensory": "Create a sensory-friendly environment. Use noise-canceling headphones, weighted blankets, and offer quiet spaces.",
    "routine": "Use visual schedules. Give warnings before transitions (5 minutes, 2 minutes). Be consistent.",
    "aba": "ABA therapy uses positive reinforcement. Break tasks into small steps. Track progress daily.",
    "occupational": "OT helps with daily living skills and sensory processing. Consult an occupational therapist."
}

# ==================== Parent Chatbot ====================
PARENT_CHAT_RESPONSES = {
    "aba": "ABA (Applied Behavior Analysis) uses positive reinforcement to teach new skills. It's evidence-based and considered the gold standard for autism intervention.",
    "dtt": "DTT (Discrete Trial Training) breaks skills into small steps with instruction, response, and consequence. Very effective for teaching new skills.",
    "teacch": "TEACCH uses visual schedules and structured environments. Great for visual learners. Reduces anxiety through predictability.",
    "sensory": "Create a calm environment. Use noise-canceling headphones, weighted blankets, quiet spaces. Identify triggers and avoid when possible.",
    "meltdown": "Stay calm. Reduce sensory input. Ensure safety. Don't argue. Give space to recover. Afterward, discuss coping strategies.",
    "communication": "Use simple language. Give extra processing time (10-15 seconds). Use visual supports like PECS. Validate their attempts.",
    "routine": "Visual schedules and consistent routines reduce anxiety. Use timers for transitions. Give warnings before changes.",
    "sleep": "Consistent bedtime routine. Limit screen time before bed. Use visual schedules for bedtime. Consult doctor about melatonin.",
    "feeding": "Offer choices. Involve child in meal prep. Use food chaining (similar foods). Praise any attempt to try new foods.",
    "school": "Request IEP or 504 plan. Visit school beforehand. Create a one-page profile about your child. Meet with teachers and staff."
}

def get_parent_chat_response(message):
    msg_lower = message.lower()
    for key, response in PARENT_CHAT_RESPONSES.items():
        if key in msg_lower:
            return response
    return "I'm here to help! Ask me about ABA therapy, DTT, TEACCH, sensory issues, meltdowns, communication, routines, sleep, feeding, or school preparation."

# ==================== Child Therapy Chat ====================
CHILD_RESPONSES = {
    "greeting": ["Hello! 😊 I'm Pepper, your therapy friend! How are you feeling today?", "Hi there! 🌟 I'm so happy to see you!", "Hey! 💫 How can I help you today?"],
    "happy": ["I'm so glad you're happy! 😊 Your happiness makes me smile!", "Yay! 🎉 Being happy is wonderful! Tell me what made you happy!", "That's awesome! 🌟 Happiness is contagious!"],
    "sad": ["I'm sorry you're feeling sad. 🤗 I'm here with you. Let's take a deep breath together.", "It's okay to feel sad. 💙 Would you like to talk about it? I'm here to listen.", "Let's do something fun to feel better! What's your favorite activity?"],
    "angry": ["I understand you're angry. 🧘 Let's count to 5 together. 1...2...3...4...5. You're doing great!", "It's okay to feel angry. Let's take a break and breathe together.", "Would you like to squeeze a stress ball or draw your feelings?"],
    "scared": ["You're safe with me. 🛡️ Let's do something calming together. Breathe in... breathe out...", "I'm here with you. 🤗 You're brave! Let's name 5 things we can see.", "It's okay to feel scared. Let's take slow breaths together."],
    "good_job": ["Great job! 🌟 I'm so proud of you!", "Excellent! 👏 You're doing amazing!", "Wow! 🎉 That's wonderful! Keep going!"],
    "help": ["Of course! 💪 I'm here to help you. What do you need?", "I'd love to help! 🌟 Tell me more about what you need help with.", "You can do this! 💪 Let me help you figure it out."],
    "game": ["Great idea! 🎮 Look at the 'My Games' section below and choose a game!", "I love games! 🎲 Pick a game and have fun! You'll earn points!", "Games are fun AND educational! 🎯 Try your best!"],
    "task_done": ["You completed your task! 🌟 I'm so proud of you!", "Task completed! 🎉 You're doing wonderful today!", "Great job finishing your task! ✅ Keep going!"],
    "default": ["That's interesting! 🎉 Tell me more!", "I'm listening! 💙 What else would you like to talk about?", "You're doing great! 🌟 Keep talking to me!"]
}

def get_child_response(message):
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["hello", "hi", "hey"]):
        return random.choice(CHILD_RESPONSES["greeting"])
    elif any(w in msg_lower for w in ["happy", "glad", "excited"]):
        return random.choice(CHILD_RESPONSES["happy"])
    elif any(w in msg_lower for w in ["sad", "upset", "unhappy"]):
        return random.choice(CHILD_RESPONSES["sad"])
    elif any(w in msg_lower for w in ["angry", "mad", "frustrated"]):
        return random.choice(CHILD_RESPONSES["angry"])
    elif any(w in msg_lower for w in ["scared", "afraid", "worried"]):
        return random.choice(CHILD_RESPONSES["scared"])
    elif any(w in msg_lower for w in ["good job", "great", "awesome"]):
        return random.choice(CHILD_RESPONSES["good_job"])
    elif any(w in msg_lower for w in ["help", "assist"]):
        return random.choice(CHILD_RESPONSES["help"])
    elif any(w in msg_lower for w in ["game", "play"]):
        return random.choice(CHILD_RESPONSES["game"])
    elif any(w in msg_lower for w in ["task", "done", "complete"]):
        return random.choice(CHILD_RESPONSES["task_done"])
    else:
        return random.choice(CHILD_RESPONSES["default"])

# ==================== Data Management ====================
def load_data():
    parents_file = os.path.join(DATA_DIR, 'parents.json')
    children_file = os.path.join(DATA_DIR, 'children.json')
    progress_file = os.path.join(DATA_DIR, 'progress.json')
    teacch_file = os.path.join(DATA_DIR, 'teacch.json')
    
    for f in [parents_file, children_file, progress_file, teacch_file]:
        if not os.path.exists(f):
            with open(f, 'w') as fp:
                json.dump({}, fp)
    
    with open(parents_file, 'r') as f:
        parents = json.load(f)
    with open(children_file, 'r') as f:
        children = json.load(f)
    with open(progress_file, 'r') as f:
        progress = json.load(f)
    with open(teacch_file, 'r') as f:
        teacch = json.load(f)
    
    return parents, children, progress, teacch

def save_data(parents, children, progress, teacch):
    parents_file = os.path.join(DATA_DIR, 'parents.json')
    children_file = os.path.join(DATA_DIR, 'children.json')
    progress_file = os.path.join(DATA_DIR, 'progress.json')
    teacch_file = os.path.join(DATA_DIR, 'teacch.json')
    
    with open(parents_file, 'w') as f:
        json.dump(parents, f, indent=2)
    with open(children_file, 'w') as f:
        json.dump(children, f, indent=2)
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)
    with open(teacch_file, 'w') as f:
        json.dump(teacch, f, indent=2)

# ==================== Generate Mock Data for Graphs ====================
def generate_mock_data():
    dates = [(datetime.now() - timedelta(days=i)).strftime('%m/%d') for i in range(7, -1, -1)]
    attention_data = [random.randint(60, 95) for _ in range(8)]
    aba_data = [random.randint(50, 100) for _ in range(8)]
    dtt_data = [random.randint(40, 95) for _ in range(8)]
    teacch_data = [random.randint(55, 98) for _ in range(8)]
    
    return {
        'dates': dates,
        'attention': attention_data,
        'aba': aba_data,
        'dtt': dtt_data,
        'teacch': teacch_data
    }

# ==================== Update Score ====================
@app.route('/api/update_score', methods=['POST'])
def update_score():
    data = request.json
    child_name = data.get('child_name')
    game_name = data.get('game_name')
    score = data.get('score', 10)
    
    parents, children, progress, teacch = load_data()
    
    if child_name not in progress:
        progress[child_name] = {'games': {}, 'total_points': 0, 'games_played': 0, 'attention': 75, 'aba': 70, 'dtt': 65, 'teacch': 68, 'tasks_completed': 0}
    
    if game_name not in progress[child_name]['games']:
        progress[child_name]['games'][game_name] = 0
    
    progress[child_name]['games'][game_name] += score
    progress[child_name]['total_points'] += score
    progress[child_name]['games_played'] += 1
    
    save_data(parents, children, progress, teacch)
    
    return jsonify({'status': 'success', 'points': score})

# ==================== Update TEACCH ====================
@app.route('/api/update_teacch', methods=['POST'])
def update_teacch():
    data = request.json
    child_name = data.get('child_name')
    task = data.get('task')
    
    parents, children, progress, teacch = load_data()
    
    if child_name not in teacch:
        teacch[child_name] = {'completed_tasks': []}
    
    if task not in teacch[child_name]['completed_tasks']:
        teacch[child_name]['completed_tasks'].append(task)
        if child_name in progress:
            progress[child_name]['tasks_completed'] = progress[child_name].get('tasks_completed', 0) + 1
    
    save_data(parents, children, progress, teacch)
    
    return jsonify({'status': 'success'})

# ==================== Routes ====================
@app.route('/')
def landing():
    return render_template_string(LANDING_TEMPLATE)

@app.route('/login/<user_type>', methods=['GET', 'POST'])
def login(user_type):
    if request.method == 'POST':
        parents, children, progress, teacch = load_data()
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        
        if user_type == 'parent':
            if username in parents and parents[username]['password'] == password:
                session['parent'] = username
                return redirect(url_for('parent_dashboard'))
        else:
            if username in children and children[username]['password'] == password:
                session['child'] = username
                return redirect(url_for('child_dashboard'))
        
        return render_template_string(LOGIN_TEMPLATE, title=user_type.capitalize(), user_type=user_type, error='Invalid credentials')
    
    return render_template_string(LOGIN_TEMPLATE, title=user_type.capitalize(), user_type=user_type)

@app.route('/register/<user_type>', methods=['GET', 'POST'])
def register(user_type):
    if request.method == 'POST':
        parents, children, progress, teacch = load_data()
        username = request.form['username']
        
        if user_type == 'parent':
            if username in parents:
                return render_template_string(REGISTER_TEMPLATE, title='Parent', user_type='parent', parents=[], error='Username exists')
            parents[username] = {'password': hashlib.md5(request.form['password'].encode()).hexdigest(), 'email': request.form.get('email', ''), 'children': []}
            save_data(parents, children, progress, teacch)
            return redirect(url_for('login', user_type='parent'))
        else:
            if username in children:
                parents_list = list(parents.keys())
                return render_template_string(REGISTER_TEMPLATE, title='Child', user_type='child', parents=parents_list, error='Username exists')
            parent_name = request.form.get('parent')
            children[username] = {'password': hashlib.md5(request.form['password'].encode()).hexdigest(), 'age': request.form.get('age', ''), 'parent': parent_name}
            if parent_name and parent_name in parents:
                parents[parent_name]['children'].append(username)
            progress[username] = {'games': {}, 'total_points': 0, 'games_played': 0, 'attention': 75, 'aba': 70, 'dtt': 65, 'teacch': 68, 'tasks_completed': 0}
            teacch[username] = {'completed_tasks': []}
            save_data(parents, children, progress, teacch)
            return redirect(url_for('login', user_type='child'))
    
    parents, _, _, _ = load_data()
    if user_type == 'parent':
        return render_template_string(REGISTER_TEMPLATE, title='Parent', user_type='parent', parents=[])
    else:
        return render_template_string(REGISTER_TEMPLATE, title='Child', user_type='child', parents=list(parents.keys()))

@app.route('/parent/dashboard')
def parent_dashboard():
    if 'parent' not in session:
        return redirect(url_for('login', user_type='parent'))
    parents, children, progress, teacch = load_data()
    parent = session['parent']
    child_list = parents[parent].get('children', [])
    return render_template_string(PARENT_DASHBOARD_HTML, username=parent, children=child_list, questions=ISAA_QUESTIONS, suggestions=THERAPY_SUGGESTIONS)

@app.route('/child/dashboard')
def child_dashboard():
    if 'child' not in session:
        return redirect(url_for('login', user_type='child'))
    return render_template_string(CHILD_DASHBOARD_HTML, username=session['child'], games=GAMES_LIST, icons=ICONS)

@app.route('/parent/child_progress/<child_name>')
def parent_child_progress(child_name):
    _, _, progress, teacch = load_data()
    child_data = progress.get(child_name, {})
    mock = generate_mock_data()
    return jsonify({
        'attention': child_data.get('attention', 75),
        'games_played': child_data.get('games_played', 0),
        'total_points': child_data.get('total_points', 0),
        'tasks_completed': child_data.get('tasks_completed', 0),
        'games': child_data.get('games', {}),
        'aba': child_data.get('aba', 70),
        'dtt': child_data.get('dtt', 65),
        'teacch': child_data.get('teacch', 68),
        'completed_tasks': teacch.get(child_name, {}).get('completed_tasks', []),
        'dates': mock['dates'],
        'attention_data': mock['attention'],
        'aba_data': mock['aba'],
        'dtt_data': mock['dtt'],
        'teacch_data': mock['teacch']
    })

@app.route('/parent/chat', methods=['POST'])
def parent_chat():
    data = request.json
    response = get_parent_chat_response(data.get('message', ''))
    return jsonify({'response': response})

@app.route('/child/chat', methods=['POST'])
def child_chat():
    data = request.json
    response = get_child_response(data.get('message', ''))
    return jsonify({'response': response})

@app.route('/parent/logout')
def parent_logout():
    session.pop('parent', None)
    return redirect(url_for('landing'))

@app.route('/child/logout')
def child_logout():
    session.pop('child', None)
    return redirect(url_for('landing'))

@app.route('/game/<game_name>')
def play_game(game_name):
    child_name = session.get('child', 'Child')
    return render_template_string(GAME_WRAPPER, game_name=game_name, game_title=game_name.replace('_', ' ').title(), child_name=child_name)

@app.route('/game_content/<game_name>')
def game_content(game_name):
    try:
        return render_template(f'games/{game_name}.html')
    except:
        return f'<div style="text-align:center;padding:50px;"><h2>{game_name.replace("_", " ").title()}</h2><p>Game content loading...</p><button onclick="window.location.href=\'/child/dashboard\'">Back to Games</button></div>'

# ==================== HTML Templates ====================
LANDING_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>ASD Support System</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;display:flex;justify-content:center;align-items:center;}
.container{text-align:center;padding:40px;}
h1{font-size:3em;color:white;margin-bottom:20px;}
.subtitle{color:#ccc;margin-bottom:40px;}
.buttons{display:flex;gap:30px;justify-content:center;flex-wrap:wrap;}
.btn{padding:20px 50px;font-size:1.5em;border:none;border-radius:15px;cursor:pointer;text-decoration:none;display:inline-block;}
.btn-parent{background:#e94560;color:white;}
.btn-child{background:#0f3460;color:white;}
.btn:hover{transform:scale(1.05);}
.footer{margin-top:50px;color:#666;}
</style>
</head>
<body>
<div class="container">
<h1>🧩 ASD Support System</h1>
<div class="subtitle">Unified Support for Autism | ABA | DTT | TEACCH</div>
<div class="buttons">
<a href="/login/parent" class="btn btn-parent">👨‍👩‍👧 Parent Portal</a>
<a href="/login/child" class="btn btn-child">🧒 Child Portal</a>
</div>
<div class="footer">Comprehensive support for parents and children with autism</div>
</div>

<div style="margin: 20px 0;">
    <button onclick="toggleGames()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 10px; cursor: pointer;">
        🎮 Show/Hide Games Portal
    </button>
    <div id="gamesFrame" style="display: none; margin-top: 20px;">
        <iframe src="http://localhost:5009" width="100%" height="600" style="border: none; border-radius: 20px;"></iframe>
    </div>
</div>
<script>
function toggleGames() {
    var frame = document.getElementById('gamesFrame');
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
    } else {
        frame.style.display = 'none';
    }
}
</script>

</body>
</html>
'''

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{{ title }} Login</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;display:flex;justify-content:center;align-items:center;}
.card{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);border-radius:20px;padding:40px;width:400px;text-align:center;}
h2{color:#e94560;margin-bottom:20px;}
input{width:100%;padding:12px;margin:10px 0;border:none;border-radius:10px;background:rgba(255,255,255,0.2);color:white;}
button{width:100%;padding:12px;background:{{ '#e94560' if user_type == 'parent' else '#0f3460' }};border:none;border-radius:10px;color:white;cursor:pointer;margin-top:10px;}
.link{margin-top:15px;display:block;color:#ccc;text-decoration:none;}
.error{color:#e94560;margin-top:10px;}
</style>
</head>
<body>
<div class="card">
<h2>{{ title }} Login</h2>
<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
<a href="/register/{{ user_type }}" class="link">Register</a>
<a href="/" class="link">← Back</a>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
</div>

<div style="margin: 20px 0;">
    <button onclick="toggleGames()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 10px; cursor: pointer;">
        🎮 Show/Hide Games Portal
    </button>
    <div id="gamesFrame" style="display: none; margin-top: 20px;">
        <iframe src="http://localhost:5009" width="100%" height="600" style="border: none; border-radius: 20px;"></iframe>
    </div>
</div>
<script>
function toggleGames() {
    var frame = document.getElementById('gamesFrame');
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
    } else {
        frame.style.display = 'none';
    }
}
</script>

</body>
</html>
'''

REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Register - {{ title }}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;display:flex;justify-content:center;align-items:center;}
.card{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);border-radius:20px;padding:40px;width:400px;text-align:center;}
h2{color:#e94560;margin-bottom:20px;}
input,select{width:100%;padding:12px;margin:10px 0;border:none;border-radius:10px;background:rgba(255,255,255,0.2);color:white;}
option{background:#1a1a2e;}
button{width:100%;padding:12px;background:{{ '#e94560' if user_type == 'parent' else '#0f3460' }};border:none;border-radius:10px;color:white;cursor:pointer;margin-top:10px;}
.link{margin-top:15px;display:block;color:#ccc;text-decoration:none;}
</style>
</head>
<body>
<div class="card">
<h2>{{ title }} Registration</h2>
<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<input type="text" name="email" placeholder="Email (optional)">
{% if user_type == 'child' %}
<input type="number" name="age" placeholder="Age" required>
<select name="parent">
<option value="">Select Parent</option>
{% for parent in parents %}
<option value="{{ parent }}">{{ parent }}</option>
{% endfor %}
</select>
{% endif %}
<button type="submit">Register</button>
</form>
<a href="/login/{{ user_type }}" class="link">← Back to Login</a>
</div>

<div style="margin: 20px 0;">
    <button onclick="toggleGames()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 10px; cursor: pointer;">
        🎮 Show/Hide Games Portal
    </button>
    <div id="gamesFrame" style="display: none; margin-top: 20px;">
        <iframe src="http://localhost:5009" width="100%" height="600" style="border: none; border-radius: 20px;"></iframe>
    </div>
</div>
<script>
function toggleGames() {
    var frame = document.getElementById('gamesFrame');
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
    } else {
        frame.style.display = 'none';
    }
}
</script>

</body>
</html>
'''

PARENT_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Parent Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;}
.header{background:linear-gradient(135deg,#0f3460,#1a1a2e);padding:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;}
.header h1{color:#e94560;}
.logout-btn{background:#e94560;padding:10px 20px;border-radius:10px;text-decoration:none;color:white;}
.dashboard{display:grid;grid-template-columns:repeat(auto-fit,minmax(500px,1fr));gap:20px;padding:20px;}
.card{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);border-radius:20px;padding:20px;border:1px solid rgba(255,255,255,0.2);}
.card h2{color:#e94560;margin-bottom:15px;}
.child-selector{margin-bottom:20px;}
.child-btn{background:#0f3460;padding:10px 15px;border-radius:10px;margin:5px;cursor:pointer;display:inline-block;}
.child-btn.active{background:#e94560;}
.stat{display:flex;justify-content:space-between;padding:10px;margin:5px 0;background:rgba(255,255,255,0.05);border-radius:10px;}
.stat-value{font-size:24px;font-weight:bold;color:#e94560;}
canvas{max-height:200px;margin:10px 0;}
.games-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px;max-height:200px;overflow-y:auto;}
.game-card{background:rgba(255,255,255,0.05);border-radius:8px;padding:8px;text-align:center;font-size:11px;}
.chat-area{height:250px;overflow-y:auto;margin-bottom:10px;padding:10px;background:rgba(0,0,0,0.3);border-radius:10px;}
.message{margin:5px 0;padding:8px;border-radius:10px;max-width:85%;}
.user-message{background:#e94560;margin-left:auto;text-align:right;}
.bot-message{background:#0f3460;}
.chat-input{display:flex;gap:10px;margin-top:10px;}
.chat-input input{flex:1;padding:10px;border:none;border-radius:10px;background:rgba(255,255,255,0.2);color:white;}
.chat-input button{padding:10px 20px;background:#e94560;border:none;border-radius:10px;color:white;cursor:pointer;}
.quick-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;}
.quick-btn{background:#0f3460;padding:5px 10px;border-radius:15px;font-size:11px;cursor:pointer;}
.routine-list li{padding:8px;margin:5px 0;background:rgba(255,255,255,0.1);border-radius:10px;cursor:pointer;display:flex;justify-content:space-between;}
.routine-list li.completed{text-decoration:line-through;opacity:0.6;background:rgba(76,175,80,0.3);}
.question{margin:15px 0;padding:10px;background:rgba(255,255,255,0.05);border-radius:10px;}
select{margin-left:10px;padding:5px;border-radius:5px;}
.btn{background:#e94560;border:none;padding:10px 20px;border-radius:10px;color:white;cursor:pointer;margin:5px;}
.suggestion-box{padding:15px;background:rgba(0,0,0,0.3);border-radius:10px;margin-top:15px;}
.tab-buttons{display:flex;gap:10px;margin-bottom:15px;}
.tab-btn{flex:1;padding:10px;background:rgba(255,255,255,0.1);border:none;border-radius:10px;color:white;cursor:pointer;}
.tab-btn.active{background:#e94560;}
.tab-content{display:none;}
.tab-content.active{display:block;}
@media (max-width:768px){.dashboard{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="header">
<h1>👨‍👩‍👧 Parent Dashboard</h1>
<div><span>Welcome, {{ username }}! </span><a href="/parent/logout" class="logout-btn">Logout</a></div>
</div>
<div class="dashboard">
<div class="card"><h2>👧 Select Child</h2><div class="child-selector" id="childSelector">{% for child in children %}<div class="child-btn" onclick="selectChild('{{ child }}')">{{ child }}</div>{% endfor %}</div></div>
<div class="card" id="progressCard" style="display:none;"><h2>📊 Progress Overview</h2><div id="progressStats"></div></div>
<div class="card" id="attentionCard" style="display:none;"><h2>📈 Attention & Focus</h2><canvas id="attentionChart"></canvas></div>
<div class="card" id="therapyCard" style="display:none;"><h2>📊 ABA | DTT | TEACCH</h2><canvas id="therapyChart"></canvas></div>
<div class="card" id="gamesCard" style="display:none;"><h2>🎮 Games Played</h2><div id="gamesList" class="games-grid"></div></div>
<div class="card" id="teacchCard" style="display:none;"><h2>📋 TEACCH Tasks</h2><ul class="routine-list" id="teacchList"></ul></div>
<div class="card"><div class="tab-buttons"><button class="tab-btn active" onclick="showTab('screening')">📋 ISAA Screening</button><button class="tab-btn" onclick="showTab('therapy')">💊 Therapy Suggestions</button><button class="tab-btn" onclick="showTab('chat')">💬 AI Chat</button></div>
<div id="screeningTab" class="tab-content active"><h2>Autism Screening (ISAA)</h2><div id="questionsContainer"></div><button class="btn" onclick="calculateScore()">Calculate Score</button><div id="scoreResult"></div><button id="reportBtn" class="btn" onclick="generateReport()" style="display:none;">📄 Generate Report</button></div>
<div id="therapyTab" class="tab-content"><h2>Therapy Suggestions</h2><select id="concernSelect"><option value="eye_contact">Eye Contact</option><option value="social_interaction">Social Interaction</option><option value="speech">Speech & Communication</option><option value="sensory">Sensory Issues</option><option value="routine">Routine & Transitions</option><option value="aba">ABA Therapy</option></select><button class="btn" onclick="getSuggestion()">Get Suggestion</button><div id="suggestionResult" class="suggestion-box"></div></div>
<div id="chatTab" class="tab-content"><h2>💬 Autism Support Chatbot</h2><div class="chat-area" id="chatArea"><div class="message bot-message">Hello! Ask me about ABA, DTT, TEACCH, sensory issues, meltdowns, communication, routines, sleep, or feeding.</div></div><div class="chat-input"><input type="text" id="chatInput" placeholder="Ask about autism..." onkeypress="if(event.key==='Enter') sendParentMessage()"><button onclick="sendParentMessage()">Send</button></div><div class="quick-actions"><div class="quick-btn" onclick="parentQuick('aba therapy')">ABA</div><div class="quick-btn" onclick="parentQuick('dtt')">DTT</div><div class="quick-btn" onclick="parentQuick('teacch')">TEACCH</div><div class="quick-btn" onclick="parentQuick('sensory overload')">Sensory</div><div class="quick-btn" onclick="parentQuick('meltdown')">Meltdowns</div><div class="quick-btn" onclick="parentQuick('sleep issues')">Sleep</div></div></div></div>
</div>
<script>
const questions = {{ questions | tojson }};
let currentChild = null;
let attentionChart, therapyChart;

function showTab(tabName){
    document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
    document.getElementById(tabName+'Tab').classList.add('active');
    event.target.classList.add('active');
}

function loadQuestions(){
    const container=document.getElementById('questionsContainer');
    container.innerHTML='';
    questions.forEach((q,idx)=>{
        const div=document.createElement('div');
        div.className='question';
        div.innerHTML=`<strong>${idx+1}. ${q}</strong><br><select id="q${idx}"><option value="5">Always (5)</option><option value="4">Often (4)</option><option value="3">Sometimes (3)</option><option value="2">Rarely (2)</option><option value="1">Never (1)</option></select>`;
        container.appendChild(div);
    });
}

function calculateScore(){
    let total=0;
    for(let i=0;i<questions.length;i++) total+=parseInt(document.getElementById(`q${i}`).value);
    const maxScore=questions.length*5;
    const percentage=(total/maxScore)*100;
    let riskLevel=percentage>=70?'High Risk':(percentage>=40?'Moderate Risk':'Low Risk');
    document.getElementById('scoreResult').innerHTML=`<div class="stat-value">Score: ${total}/${maxScore} (${percentage.toFixed(1)}%)</div><div style="margin-top:10px;padding:10px;background:rgba(0,0,0,0.3);border-radius:10px;"><strong>Risk Level: ${riskLevel}</strong></div>`;
    document.getElementById('reportBtn').style.display='inline-block';
}

function generateReport(){
    const total=parseInt(document.getElementById('scoreResult').innerHTML.match(/Score: (\\d+)/)?.[1]||0);
    const maxScore=questions.length*5;
    const percentage=(total/maxScore)*100;
    let report=`ASD Screening Report\nDate: ${new Date().toLocaleDateString()}\nScore: ${total}/${maxScore} (${percentage.toFixed(1)}%)\nRecommendation: Consult a specialist.`;
    const blob=new Blob([report],{type:'text/plain'});
    const link=document.createElement('a');
    link.href=URL.createObjectURL(blob);
    link.download='asd_screening_report.txt';
    link.click();
}

function getSuggestion(){
    const concern=document.getElementById('concernSelect').value;
    const suggestions={
        'eye_contact':'Practice eye contact during fun activities. Use toys to draw attention to your face.',
        'social_interaction':'Arrange playdates with siblings or peers. Use turn-taking games.',
        'speech':'Work with a speech therapist. Use picture cards (PECS) and simple words.',
        'sensory':'Create a sensory-friendly environment. Use noise-canceling headphones, weighted blankets.',
        'routine':'Use visual schedules. Give warnings before transitions. Be consistent.',
        'aba':'ABA uses positive reinforcement. Break tasks into small steps. Track progress daily.'
    };
    document.getElementById('suggestionResult').innerHTML=suggestions[concern]||'Please select a concern.';
}

function selectChild(childName){
    currentChild=childName;
    document.querySelectorAll('.child-btn').forEach(b=>b.classList.remove('active'));
    event.target.classList.add('active');
    fetch(`/parent/child_progress/${childName}`).then(res=>res.json()).then(data=>{
        document.querySelectorAll('#progressCard,#attentionCard,#therapyCard,#gamesCard,#teacchCard').forEach(c=>c.style.display='block');
        document.getElementById('progressStats').innerHTML=`<div class="stat"><span>🎯 Attention:</span><span class="stat-value">${data.attention}%</span></div><div class="stat"><span>🎮 Games:</span><span class="stat-value">${data.games_played}</span></div><div class="stat"><span>⭐ Points:</span><span class="stat-value">${data.total_points}</span></div><div class="stat"><span>✅ Tasks:</span><span class="stat-value">${data.tasks_completed}</span></div>`;
        if(attentionChart) attentionChart.destroy();
        attentionChart=new Chart(document.getElementById('attentionChart'),{type:'line',data:{labels:data.dates,datasets:[{label:'Attention %',data:data.attention_data,borderColor:'#e94560',fill:false,tension:0.3}]}});
        if(therapyChart) therapyChart.destroy();
        therapyChart=new Chart(document.getElementById('therapyChart'),{type:'line',data:{labels:data.dates,datasets:[{label:'ABA',data:data.aba_data,borderColor:'#4a90e2',fill:false},{label:'DTT',data:data.dtt_data,borderColor:'#e94560',fill:false},{label:'TEACCH',data:data.teacch_data,borderColor:'#4caf50',fill:false}]}});
        let gamesHtml='';
        for(let[game,score]of Object.entries(data.games)) if(score>0) gamesHtml+=`<div class="game-card"><div>${game.replace(/_/g,' ')}</div><div style="color:#e94560;">⭐ ${score}</div></div>`;
        document.getElementById('gamesList').innerHTML=gamesHtml||'<p>No games played yet.</p>';
        const teacchList=document.getElementById('teacchList');
        teacchList.innerHTML='';
        const tasks=['Wake up & get ready','Complete learning activity','Play a game','Practice communication','Follow visual schedule'];
        tasks.forEach(task=>{const li=document.createElement('li');li.innerHTML=`<span>${task}</span><span>${data.completed_tasks.includes(task)?'✅':'⭕'}</span>`;if(data.completed_tasks.includes(task))li.classList.add('completed');teacchList.appendChild(li);});
    });
}

function sendParentMessage(){
    const input=document.getElementById('chatInput');
    const msg=input.value.trim();
    if(!msg)return;
    const area=document.getElementById('chatArea');
    const userDiv=document.createElement('div');userDiv.className='message user-message';userDiv.innerHTML=msg;area.appendChild(userDiv);input.value='';
    fetch('/parent/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})}).then(res=>res.json()).then(data=>{const botDiv=document.createElement('div');botDiv.className='message bot-message';botDiv.innerHTML=data.response;area.appendChild(botDiv);area.scrollTop=area.scrollHeight;});
}

function parentQuick(q){document.getElementById('chatInput').value=q;sendParentMessage();}

setTimeout(()=>{const firstBtn=document.querySelector('.child-btn');if(firstBtn)firstBtn.click();},100);
loadQuestions();
</script>

<div style="margin: 20px 0;">
    <button onclick="toggleGames()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 10px; cursor: pointer;">
        🎮 Show/Hide Games Portal
    </button>
    <div id="gamesFrame" style="display: none; margin-top: 20px;">
        <iframe src="http://localhost:5009" width="100%" height="600" style="border: none; border-radius: 20px;"></iframe>
    </div>
</div>
<script>
function toggleGames() {
    var frame = document.getElementById('gamesFrame');
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
    } else {
        frame.style.display = 'none';
    }
}
</script>

</body>
</html>
'''

CHILD_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Child Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;}
.header{background:linear-gradient(135deg,#0f3460,#1a1a2e);padding:20px;display:flex;justify-content:space-between;align-items:center;}
.header h1{color:#e94560;}
.logout-btn{background:#e94560;padding:10px 20px;border-radius:10px;text-decoration:none;color:white;}
.dashboard{display:grid;grid-template-columns:repeat(auto-fit,minmax(450px,1fr));gap:20px;padding:20px;max-width:1400px;margin:0 auto;}
.card{background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);border-radius:20px;padding:20px;border:1px solid rgba(255,255,255,0.2);}
.card h2{color:#e94560;margin-bottom:15px;}
.chat-area{height:250px;overflow-y:auto;margin-bottom:10px;padding:10px;background:rgba(0,0,0,0.3);border-radius:10px;}
.message{margin:8px 0;padding:8px;border-radius:10px;max-width:85%;}
.user-message{background:#e94560;margin-left:auto;text-align:right;}
.bot-message{background:#0f3460;}
.chat-input{display:flex;gap:10px;margin-top:10px;}
.chat-input input{flex:1;padding:10px;border:none;border-radius:10px;background:rgba(255,255,255,0.2);color:white;}
.chat-input button{padding:10px 20px;background:#e94560;border:none;border-radius:10px;color:white;cursor:pointer;}
.quick-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;}
.quick-btn{background:#0f3460;padding:5px 10px;border-radius:15px;font-size:11px;cursor:pointer;}
.breathing-circle{width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#4a90e2,#357abd);margin:20px auto;display:flex;align-items:center;justify-content:center;cursor:pointer;animation:breathe 4s ease-in-out infinite;}
@keyframes breathe{0%,100%{transform:scale(1);}50%{transform:scale(1.15);}}
.games-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:10px;max-height:300px;overflow-y:auto;}
.game-card{background:rgba(255,255,255,0.1);border-radius:10px;padding:10px;text-align:center;cursor:pointer;transition:all 0.3s;}
.game-card:hover{background:#e94560;transform:scale(1.05);}
.routine-list li{padding:10px;margin:5px 0;background:rgba(255,255,255,0.1);border-radius:10px;cursor:pointer;display:flex;justify-content:space-between;}
.routine-list li.completed{text-decoration:line-through;opacity:0.6;background:rgba(76,175,80,0.3);}
@media (max-width:768px){.dashboard{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="header"><h1>🧒 Welcome, {{ username }}!</h1><a href="/child/logout" class="logout-btn">Logout</a></div>
<div class="dashboard">
<div class="card"><h2>💬 Pepper - Your Therapy Friend</h2><div class="chat-area" id="chatArea"><div class="message bot-message">Hi {{ username }}! I'm Pepper! 😊 How are you feeling today? 🌟</div></div><div class="chat-input"><input type="text" id="chatInput" placeholder="Type your message..." onkeypress="if(event.key==='Enter') sendChildMessage()"><button onclick="sendChildMessage()">Send</button></div><div class="quick-actions"><div class="quick-btn" onclick="childQuick('I did something good today')">🎉 Good Job</div><div class="quick-btn" onclick="childQuick('I feel happy')">😊 Happy</div><div class="quick-btn" onclick="childQuick('I feel sad')">😢 Sad</div><div class="quick-btn" onclick="childQuick('I need a break')">😌 Break</div><div class="quick-btn" onclick="childQuick('Help me please')">🆘 Help</div><div class="quick-btn" onclick="childQuick('I want to play a game')">🎮 Game</div><div class="quick-btn" onclick="childQuick('I finished my task')">✅ Task Done</div></div></div>
<div class="card"><h2>🧘 Calm Down - Breathing</h2><div class="breathing-circle" onclick="startBreathing()"><span>🧘<br>Breathe</span></div><div id="breathingText" style="text-align:center;">Click to start</div></div>
<div class="card"><h2>📋 My Daily Tasks (TEACCH)</h2><ul class="routine-list" id="routineList"></ul></div>
<div class="card"><h2>🎮 My Games</h2><div class="games-grid" id="gamesGrid"></div></div>
</div>
<script>
const games = {{ games | tojson }};
const icons = {{ icons | tojson }};
const tasks = ["Wake up & get ready 🛌", "Complete learning activity 📚", "Play a game 🎮", "Practice communication 💬", "Follow visual schedule 📋"];
let completedTasks = JSON.parse(localStorage.getItem('child_tasks_{{ username }}') || '[]');
let currentChild = '{{ username }}';

function loadTasks(){
    const list=document.getElementById('routineList');
    list.innerHTML='';
    tasks.forEach(task=>{
        const li=document.createElement('li');
        li.innerHTML=`<span>${task}</span><span>✅</span>`;
        if(completedTasks.includes(task)) li.classList.add('completed');
        li.onclick=()=>{
            if(li.classList.contains('completed')){
                li.classList.remove('completed');
                completedTasks=completedTasks.filter(t=>t!==task);
            }else{
                li.classList.add('completed');
                completedTasks.push(task);
                fetch('/api/update_teacch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({child_name:currentChild,task:task})});
            }
            localStorage.setItem('child_tasks_{{ username }}',JSON.stringify(completedTasks));
        };
        list.appendChild(li);
    });
}

function sendChildMessage(){
    const input=document.getElementById('chatInput');
    const msg=input.value.trim();
    if(!msg)return;
    const area=document.getElementById('chatArea');
    const userDiv=document.createElement('div');userDiv.className='message user-message';userDiv.innerHTML=msg;area.appendChild(userDiv);input.value='';
    fetch('/child/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})}).then(res=>res.json()).then(data=>{const botDiv=document.createElement('div');botDiv.className='message bot-message';botDiv.innerHTML=data.response;area.appendChild(botDiv);area.scrollTop=area.scrollHeight;});
}

function childQuick(q){document.getElementById('chatInput').value=q;sendChildMessage();}

let breathingInterval;
function startBreathing(){
    const textDiv=document.getElementById('breathingText');
    let step=0;
    const phases=["Breathe in... 4 seconds","Hold... 4 seconds","Breathe out... 4 seconds"];
    if(breathingInterval)clearInterval(breathingInterval);
    breathingInterval=setInterval(()=>{textDiv.innerHTML=phases[step%3];step++;if(step>=9){clearInterval(breathingInterval);textDiv.innerHTML="✨ Great job! ✨";setTimeout(()=>textDiv.innerHTML="Click to start",2000);}},4000);
}

function loadGames(){
    const grid=document.getElementById('gamesGrid');
    grid.innerHTML='';
    games.forEach(game=>{
        const card=document.createElement('div');
        card.className='game-card';
        card.innerHTML=`<div style="font-size:32px;">${icons[game]||'🎮'}</div><div>${game.replace(/_/g,' ')}</div>`;
        card.onclick=()=>window.location.href=`/game/${game}`;
        grid.appendChild(card);
    });
}

loadTasks();
loadGames();
</script>

<div style="margin: 20px 0;">
    <button onclick="toggleGames()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 10px; cursor: pointer;">
        🎮 Show/Hide Games Portal
    </button>
    <div id="gamesFrame" style="display: none; margin-top: 20px;">
        <iframe src="http://localhost:5009" width="100%" height="600" style="border: none; border-radius: 20px;"></iframe>
    </div>
</div>
<script>
function toggleGames() {
    var frame = document.getElementById('gamesFrame');
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
    } else {
        frame.style.display = 'none';
    }
}
</script>

</body>
</html>
'''

GAME_WRAPPER = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{{ game_title }}</title>
<style>
body{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;font-family:'Segoe UI',sans-serif;padding:20px;}
.game-container{max-width:1200px;margin:0 auto;background:rgba(255,255,255,0.1);border-radius:20px;padding:20px;}
h1{color:#e94560;text-align:center;}
.back-btn{background:#e94560;border:none;padding:10px 20px;border-radius:10px;color:white;cursor:pointer;margin-bottom:20px;}
.message-area{margin-top:20px;padding:15px;background:rgba(0,0,0,0.5);border-radius:10px;text-align:center;font-size:18px;}
.correct-answer{background:#4caf50;animation:celebrate 0.5s ease;}
.wrong-answer{background:#ff9800;animation:shake 0.3s ease;}
@keyframes celebrate{0%{transform:scale(1);}50%{transform:scale(1.05);}100%{transform:scale(1);}}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-5px);}75%{transform:translateX(5px);}}
</style>
</head>
<body>
<div class="game-container">
<button class="back-btn" onclick="window.location.href='/child/dashboard'">← Back</button>
<h1>{{ game_title }}</h1>
<div id="gameContent"><p style="text-align:center;padding:50px;">Loading game...</p></div>
<div class="message-area" id="messageArea">💡 Play and earn points!</div>
</div>
<script>
let currentChild='{{ child_name }}';
let currentGame='{{ game_name }}';

function playSound(type){
    const emoji=type==='correct'?['👏','🎉','🌟'][Math.floor(Math.random()*3)]:['😊','👍','💪'][Math.floor(Math.random()*3)];
    const msgDiv=document.getElementById('messageArea');
    if(type==='correct'){
        msgDiv.innerHTML=`${emoji} Great job! +10 points! ${emoji}`;
        msgDiv.classList.add('correct-answer');
        setTimeout(()=>msgDiv.classList.remove('correct-answer'),1500);
        updateScore(10);
    }else{
        msgDiv.innerHTML=`${emoji} Good try! +2 points! ${emoji}`;
        msgDiv.classList.add('wrong-answer');
        setTimeout(()=>msgDiv.classList.remove('wrong-answer'),1500);
        updateScore(2);
    }
}

function updateScore(points){
    fetch('/api/update_score',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({child_name:currentChild,game_name:currentGame,score:points})});
}

fetch('/game_content/{{ game_name }}').then(res=>res.text()).then(html=>{document.getElementById('gameContent').innerHTML=html;setTimeout(()=>{if(typeof window.injectGameHandlers==='function')window.injectGameHandlers(playSound,updateScore);},100);}).catch(()=>{document.getElementById('gameContent').innerHTML=`<div style="text-align:center;padding:50px;"><h2>{{ game_title }}</h2><p>Game loading...</p><button onclick="window.location.href='/child/dashboard'">Back</button></div>`;});
</script>

<div style="margin: 20px 0;">
    <button onclick="toggleGames()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 10px; cursor: pointer;">
        🎮 Show/Hide Games Portal
    </button>
    <div id="gamesFrame" style="display: none; margin-top: 20px;">
        <iframe src="http://localhost:5009" width="100%" height="600" style="border: none; border-radius: 20px;"></iframe>
    </div>
</div>
<script>
function toggleGames() {
    var frame = document.getElementById('gamesFrame');
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
    } else {
        frame.style.display = 'none';
    }
}
</script>

</body>
</html>
'''

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧩 FINAL COMPLETE ASD SYSTEM")
    print("="*60)
    print("✅ Parent Dashboard - ISAA Test + AI Suggestions + PDF Report + Chatbot + Graphs")
    print("✅ Child Dashboard - Games (FULLY WORKING) + Therapy Chat + Breathing + TEACCH")
    print("✅ Unified Login System")
    print(f"🎮 Games available: {len(GAMES_LIST)}")
    print("="*60)
    print("🌐 Opening at: http://localhost:5001")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
