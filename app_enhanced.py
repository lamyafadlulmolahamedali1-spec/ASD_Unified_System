#!/usr/bin/env python3
"""
ASD Complete System - ENHANCED VERSION
- TEACCH Schedule with Full Dashboard Integration
- Autism Support Chatbot (لأسئلة الآباء)
- Breathing Exercise
- Daily Routine Manager
- Progress Tracking
- Games Dashboard
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import random
import threading
import time
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'asd_complete_key'

DATA_DIR = '/home/lamya/Desktop/ASD_Complete_Project_20260325_161142/data'
os.makedirs(DATA_DIR, exist_ok=True)

# ==================== Autism Knowledge Base (للآباء) ====================
AUTISM_KNOWLEDGE = {
    "what is autism": "Autism Spectrum Disorder (ASD) is a developmental condition that affects communication, behavior, and social interaction. Each person with autism is unique with their own strengths and challenges.",
    "signs of autism": "Common early signs include: delayed speech, avoiding eye contact, not responding to name, repetitive movements (hand flapping, rocking), sensory sensitivities, and difficulty with social interactions.",
    "aba therapy": "ABA (Applied Behavior Analysis) uses positive reinforcement to teach new skills and reduce challenging behaviors. It's evidence-based and considered the gold standard for autism intervention.",
    "speech therapy": "Speech therapy helps with communication skills, including verbal and non-verbal communication, articulation, and social language. Early intervention is key.",
    "occupational therapy": "Occupational therapy (OT) helps with sensory processing, fine motor skills, daily living skills (dressing, eating), and self-regulation.",
    "how to handle meltdown": "Stay calm. Reduce sensory input (lights, sounds, people). Ensure safety. Don't argue or punish. Give space and time to recover. Afterward, talk about coping strategies.",
    "sensory overload": "Signs include covering ears, hiding, crying, aggression. Help by: reducing stimuli, moving to a quiet space, offering deep pressure, using noise-canceling headphones, weighted blankets.",
    "routine importance": "Routines provide predictability and reduce anxiety. Use visual schedules. Warn before transitions. Keep consistent daily patterns for meals, sleep, and activities.",
    "how to communicate": "Use simple, clear language. Give extra time to process (10-15 seconds). Use visual supports (PECS, pictures). Be patient and listen actively. Validate their feelings.",
    "early intervention": "Early intervention (before age 3) greatly improves outcomes. Seek evaluation if concerned. Services may include speech, OT, ABA, and developmental therapy.",
    "pecs": "PECS (Picture Exchange Communication System) is a visual communication system where the child exchanges pictures to communicate needs, wants, and thoughts.",
    "visual schedule": "Visual schedules use pictures or words to show what will happen. They help with transitions and reduce anxiety. Place them at eye level.",
    "parent support": "Take care of yourself too! Join support groups, seek respite care, connect with other parents. Your well-being matters for your child's well-being.",
    "school preparation": "Visit the school beforehand. Create a one-page profile about your child. Meet with teachers and support staff. Practice routines at home. Use social stories.",
    "social stories": "Social stories are short descriptions of social situations. They help children understand what to expect and how to respond. Customize for your child.",
    "stimming": "Stimming (repetitive movements) helps with self-regulation. It's not harmful unless it causes injury. Redirect rather than stop completely.",
    "eye contact": "Don't force eye contact. It can be uncomfortable or painful. Use alternative ways to show attention like looking near the face or using verbal cues."
}

# ==================== Daily Routines ====================
DAILY_ROUTINES = {
    "morning": ["Wake up 🛌", "Brush teeth 🪥", "Wash face 🧼", "Get dressed 👕", "Eat breakfast 🍳", "Pack bag 🎒"],
    "afternoon": ["Learning time 📚", "Play time 🎮", "Eat lunch 🍎", "Rest time 😴", "Outdoor walk 🚶"],
    "evening": ["Eat dinner 🍽️", "Bath time 🛁", "Read story 📖", "Brush teeth 🪥", "Bedtime 😴"]
}

# ==================== Breathing Exercises ====================
BREATHING_EXERCISES = {
    "4-4-4": {"in": 4, "hold": 4, "out": 4, "name": "Calming Breath"},
    "4-7-8": {"in": 4, "hold": 7, "out": 8, "name": "Relaxing Breath"},
    "square": {"in": 4, "hold": 4, "out": 4, "hold2": 4, "name": "Square Breathing"}
}

# ==================== قائمة الألعاب ====================
games_dir = os.path.join(os.path.dirname(__file__), 'templates', 'games')
exclude = {'landing', 'parent_login', 'parent_register', 'child_login', 'games_menu', 'parent_dashboard', 'index'}

GAMES_LIST = []
if os.path.exists(games_dir):
    for f in os.listdir(games_dir):
        if f.endswith('.html') and os.path.splitext(f)[0] not in exclude:
            GAMES_LIST.append(os.path.splitext(f)[0])
GAMES_LIST = list(set(GAMES_LIST))
GAMES_LIST.sort()

print(f"✅ تم تحميل {len(GAMES_LIST)} لعبة")

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

# ==================== البيانات ====================
users_file = os.path.join(DATA_DIR, 'users.json')
progress_file = os.path.join(DATA_DIR, 'progress.json')
therapy_file = os.path.join(DATA_DIR, 'therapy.json')
sessions_file = os.path.join(DATA_DIR, 'sessions.json')
child_state_file = os.path.join(DATA_DIR, 'child_state.json')
teacch_file = os.path.join(DATA_DIR, 'teacch.json')

def load_json(f):
    if os.path.exists(f):
        with open(f, 'r') as fp:
            return json.load(fp)
    return {}

def save_json(f, data):
    with open(f, 'w') as fp:
        json.dump(data, fp, indent=2)

def init_child(child, age):
    prog = load_json(progress_file)
    if child not in prog:
        prog[child] = {'age': age, 'games': {}}
        for g in GAMES_LIST:
            prog[child]['games'][g] = {'played':0, 'correct':0, 'wrong':0, 'score':0, 'accuracy':0}
        save_json(progress_file, prog)
    
    therapy = load_json(therapy_file)
    if child not in therapy:
        therapy[child] = {
            'aba_stats': {'positive':0, 'calming':0, 'instructions':0},
            'attention_history': [0.5],
            'emotion_history': ['neutral'],
            'behaviour_history': ['normal'],
            'teacch_completed': []
        }
        save_json(therapy_file, therapy)
    
    sessions = load_json(sessions_file)
    if child not in sessions:
        sessions[child] = []
        save_json(sessions_file, sessions)
    
    state = load_json(child_state_file)
    if child not in state:
        state[child] = {'emotion': 'neutral', 'attention': 0.5, 'behaviour': 'normal', 'arousal': 0.5}
        save_json(child_state_file, state)
    
    teacch = load_json(teacch_file)
    if child not in teacch:
        teacch[child] = {'schedule': [], 'completed': []}
        save_json(teacch_file, teacch)

# ==================== Routes ====================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """API للشات بوت - يجيب على أسئلة الآباء عن التوحد"""
    data = request.json
    question = data.get('question', '').lower()
    
    for key, answer in AUTISM_KNOWLEDGE.items():
        if key in question:
            return jsonify({'response': answer})
    
    return jsonify({'response': "I'm here to help! Ask me about autism signs, therapies (ABA, speech, OT), communication, sensory needs, meltdowns, routines, or early intervention."})

@app.route('/routine/<time_of_day>', methods=['GET'])
def get_routine(time_of_day):
    """جلب جدول المهام اليومي"""
    return jsonify(DAILY_ROUTINES.get(time_of_day, DAILY_ROUTINES['morning']))

@app.route('/breathing/<exercise_type>', methods=['GET'])
def get_breathing(exercise_type):
    """جلب تمارين التنفس"""
    return jsonify(BREATHING_EXERCISES.get(exercise_type, BREATHING_EXERCISES['4-4-4']))

@app.route('/games')
def games():
    return render_template_string(GAMES_TEMPLATE, games=GAMES_LIST, icons=ICONS)

# ==================== HTML Templates ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASD Support Dashboard - Pepper Robot</title>
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
            text-align: center;
            border-bottom: 3px solid #e94560;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .header p { color: #ccc; }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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
            transition: transform 0.3s;
        }
        .card:hover { transform: translateY(-5px); }
        .card h2 {
            color: #e94560;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .chat-area {
            height: 250px;
            overflow-y: auto;
            margin-bottom: 15px;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
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
        .chat-input button, .quick-btn {
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
            gap: 10px;
            margin-top: 15px;
        }
        .quick-btn { background: #0f3460; font-size: 12px; padding: 8px 12px; }
        .routine-list { list-style: none; }
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
            margin: 5px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        .stat-value { font-size: 24px; font-weight: bold; color: #e94560; }
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
            transition: transform 0.3s;
            animation: breathe 4s ease-in-out infinite;
        }
        @keyframes breathe {
            0%, 100% { transform: scale(1); background: #4a90e2; }
            50% { transform: scale(1.2); background: #2c5f8a; }
        }
        .tab-buttons { display: flex; gap: 10px; margin-bottom: 15px; }
        .tab-btn {
            flex: 1;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
        }
        .tab-btn.active { background: #e94560; }
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
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
        .game-card:hover { background: #e94560; transform: scale(1.05); }
        @media (max-width: 768px) { .dashboard { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧩 ASD Support Dashboard - Pepper Robot</h1>
        <p>Support for Parents & Children | ABA | TEACCH | PECS | Sensory Support | Games</p>
    </div>
    
    <div class="dashboard">
        <!-- Card 1: AI Chatbot for Parents -->
        <div class="card">
            <h2>💬 Autism Support Chatbot</h2>
            <div class="chat-area" id="chatArea">
                <div class="message bot-message">Hello! I'm your Autism Support Assistant. Ask me anything about autism, therapies, communication, sensory needs, or daily routines.</div>
            </div>
            <div class="chat-input">
                <input type="text" id="chatInput" placeholder="Ask about autism, therapy, communication..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Send</button>
            </div>
            <div class="quick-actions">
                <button class="quick-btn" onclick="quickQuestion('what is autism')">❓ What is Autism?</button>
                <button class="quick-btn" onclick="quickQuestion('signs of autism')">📋 Signs of Autism</button>
                <button class="quick-btn" onclick="quickQuestion('how to handle meltdown')">😔 Meltdown Help</button>
                <button class="quick-btn" onclick="quickQuestion('aba therapy')">📚 ABA Therapy</button>
                <button class="quick-btn" onclick="quickQuestion('sensory overload')">🌊 Sensory Overload</button>
                <button class="quick-btn" onclick="quickQuestion('routine importance')">📅 Routine Tips</button>
            </div>
        </div>
        
        <!-- Card 2: Daily Routine -->
        <div class="card">
            <h2>📋 Daily Routine</h2>
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="showRoutineTab('morning')">🌅 Morning</button>
                <button class="tab-btn" onclick="showRoutineTab('afternoon')">☀️ Afternoon</button>
                <button class="tab-btn" onclick="showRoutineTab('evening')">🌙 Evening</button>
            </div>
            <ul class="routine-list" id="routineList"></ul>
            <div class="stat">
                <span>✅ Completed today:</span>
                <span class="stat-value" id="taskCount">0</span>
            </div>
        </div>
        
        <!-- Card 3: Breathing Exercise -->
        <div class="card">
            <h2>🧘 Calm Down - Breathing Exercise</h2>
            <div class="breathing-circle" id="breathingCircle" onclick="startBreathing()">
                <span style="text-align: center;">🧘<br>Breathe</span>
            </div>
            <div class="breathing-text" id="breathingText" style="text-align: center;">
                Click the circle to start breathing exercise
            </div>
            <div class="quick-actions">
                <button class="quick-btn" onclick="startBreathing()">Start Breathing</button>
            </div>
        </div>
        
        <!-- Card 4: Games -->
        <div class="card">
            <h2>🎮 Educational Games</h2>
            <div class="games-grid" id="gamesGrid">
                {% for game in games %}
                <div class="game-card" onclick="window.location.href='/game/{{ game }}'">
                    <div style="font-size: 32px;">{{ icons.get(game, '🎮') }}</div>
                    <div>{{ game.replace('_', ' ').title() }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <script>
        const routines = {
            morning: ["Wake up 🛌", "Brush teeth 🪥", "Wash face 🧼", "Get dressed 👕", "Eat breakfast 🍳", "Pack bag 🎒"],
            afternoon: ["Learning time 📚", "Play time 🎮", "Eat lunch 🍎", "Rest time 😴", "Outdoor walk 🚶"],
            evening: ["Eat dinner 🍽️", "Bath time 🛁", "Read story 📖", "Brush teeth 🪥", "Bedtime 😴"]
        };
        
        let currentRoutine = "morning";
        let completedTasks = localStorage.getItem("completedTasks") ? JSON.parse(localStorage.getItem("completedTasks")) : [];
        let questionCount = localStorage.getItem("questionCount") ? parseInt(localStorage.getItem("questionCount")) : 0;
        let breathingCount = localStorage.getItem("breathingCount") ? parseInt(localStorage.getItem("breathingCount")) : 0;
        
        function updateStats() {
            document.getElementById("taskCount").innerText = completedTasks.length;
        }
        
        function sendMessage() {
            const input = document.getElementById("chatInput");
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, "user");
            input.value = "";
            questionCount++;
            localStorage.setItem("questionCount", questionCount);
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: message})
            })
            .then(res => res.json())
            .then(data => {
                setTimeout(() => addMessage(data.response, "bot"), 500);
            });
        }
        
        function quickQuestion(q) {
            document.getElementById("chatInput").value = q;
            sendMessage();
        }
        
        function addMessage(text, sender) {
            const chatArea = document.getElementById("chatArea");
            const msgDiv = document.createElement("div");
            msgDiv.className = `message ${sender === "user" ? "user-message" : "bot-message"}`;
            msgDiv.innerHTML = text;
            chatArea.appendChild(msgDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function showRoutineTab(tab) {
            currentRoutine = tab;
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            updateRoutineList();
        }
        
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
        }
        
        function toggleTask(element, task) {
            if (element.classList.contains("completed")) {
                element.classList.remove("completed");
                completedTasks = completedTasks.filter(t => t !== task);
            } else {
                element.classList.add("completed");
                completedTasks.push(task);
            }
            localStorage.setItem("completedTasks", JSON.stringify(completedTasks));
            updateStats();
        }
        
        let breathingInterval;
        function startBreathing() {
            breathingCount++;
            localStorage.setItem("breathingCount", breathingCount);
            
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
        
        updateStats();
        updateRoutineList();
    </script>
</body>
</html>
'''

GAMES_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASD Games - Pepper Robot</title>
    <style>
        body {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
        }
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .game-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .game-card:hover {
            background: #e94560;
            transform: scale(1.05);
        }
        .game-icon { font-size: 48px; margin-bottom: 10px; }
        .game-name { font-size: 14px; }
        .back-btn {
            background: #e94560;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <button class="back-btn" onclick="window.location.href='/'">← Back to Dashboard</button>
    <h1 style="text-align: center;">🎮 Educational Games</h1>
    <div class="games-grid">
        {% for game in games %}
        <div class="game-card" onclick="window.location.href='/game/{{ game }}'">
            <div class="game-icon">{{ icons.get(game, '🎮') }}</div>
            <div class="game-name">{{ game.replace('_', ' ').title() }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/game/<game_name>')
def play_game(game_name):
    """تشغيل لعبة محددة"""
    return render_template(f'games/{game_name}.html')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧩 ASD ENHANCED DASHBOARD")
    print("="*50)
    print(f"📚 Autism Knowledge Base: {len(AUTISM_KNOWLEDGE)} topics")
    print(f"📋 Daily Routines: Morning, Afternoon, Evening")
    print(f"🧘 Breathing Exercises: 4-4-4, 4-7-8, Square")
    print(f"🎮 Games available: {len(GAMES_LIST)}")
    print("="*50)
    print("🌐 Opening at: http://localhost:5001")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
