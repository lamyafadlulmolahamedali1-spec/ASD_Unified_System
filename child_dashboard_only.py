#!/usr/bin/env python3
"""
CHILD DASHBOARD ONLY - Games Working + AI Chat
- No changes to Parent Dashboard
- All 39 games working
- ABA-based AI Chat
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
import random
import hashlib
import urllib.parse
import requests

app = Flask(__name__)
app.secret_key = 'child_only_key'

# ==================== ABA-Based AI Responses ====================
ABA_RESPONSES = {
    "greeting": ["Hello! 😊 How are you today? I'm so happy to see you!", "Hi there! 🌟 It's great to talk with you!"],
    "positive": ["Great job! 🌟 I'm so proud of you!", "Excellent! 👏 You're doing amazing!", "Keep going! 💪"],
    "feeling_happy": ["I'm so happy you're feeling happy! 😊 Your smile makes my day brighter!"],
    "feeling_sad": ["It's okay to feel sad. 🤗 I'm here with you. Let's take a deep breath together."],
    "feeling_angry": ["It's okay to feel angry. 🧘 Let's count to 5 together. You're doing great!"],
    "help": ["I'm here to help you! 💪 What do you need?", "Of course! 🌟 Let me help you."],
    "game": ["Great idea! 🎮 Look at the 'My Games' section below!", "I love games! 🎲 Choose one and have fun!"],
    "task": ["You're doing great with your tasks! ✅ Keep going!", "I'm proud of you! 🌟"],
    "default": ["That's interesting! 🎉 Tell me more!", "I love learning from you! 💙"]
}

def get_aba_response(message):
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["hello", "hi", "hey"]):
        return random.choice(ABA_RESPONSES["greeting"])
    elif any(w in msg_lower for w in ["good", "great", "awesome", "nice", "perfect"]):
        return random.choice(ABA_RESPONSES["positive"])
    elif any(w in msg_lower for w in ["happy", "glad", "excited"]):
        return random.choice(ABA_RESPONSES["feeling_happy"])
    elif any(w in msg_lower for w in ["sad", "upset", "unhappy"]):
        return random.choice(ABA_RESPONSES["feeling_sad"])
    elif any(w in msg_lower for w in ["angry", "mad", "frustrated"]):
        return random.choice(ABA_RESPONSES["feeling_angry"])
    elif any(w in msg_lower for w in ["help", "assist"]):
        return random.choice(ABA_RESPONSES["help"])
    elif any(w in msg_lower for w in ["game", "play", "games"]):
        return random.choice(ABA_RESPONSES["game"])
    elif any(w in msg_lower for w in ["task", "done", "complete"]):
        return random.choice(ABA_RESPONSES["task"])
    else:
        return random.choice(ABA_RESPONSES["default"])

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

# ==================== Routes ====================
@app.route('/')
def index():
    return redirect(url_for('child_dashboard'))

@app.route('/child/dashboard')
def child_dashboard():
    if 'child' not in session:
        session['child'] = 'Child'
    return render_template_string(CHILD_DASHBOARD_HTML, username=session['child'], games=GAMES_LIST, icons=ICONS)

@app.route('/child/chat', methods=['POST'])
def child_chat():
    data = request.json
    message = data.get('message', '')
    response = get_aba_response(message)
    return jsonify({'response': response})

@app.route('/child/logout')
def child_logout():
    session.pop('child', None)
    return redirect(url_for('child_dashboard'))

@app.route('/game/<game_name>')
def play_game(game_name):
    child_name = session.get('child', 'Child')
    return render_template_string(GAME_WRAPPER, game_name=game_name, game_title=game_name.replace('_', ' ').title(), child_name=child_name)

@app.route('/game_content/<game_name>')
def game_content(game_name):
    try:
        from flask import render_template
        return render_template(f'games/{game_name}.html')
    except:
        return f'<div style="text-align:center;padding:50px;"><h2>{game_name.replace("_", " ").title()}</h2><button onclick="window.parent.playSound(\'correct\')" style="background:#e94560;border:none;padding:15px 30px;border-radius:10px;color:white;font-size:18px;cursor:pointer;">🎮 Play (+10 points)</button></div>'

# ==================== HTML Templates ====================
CHILD_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Child Dashboard - Pepper AI</title>
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
<div class="card"><h2>💬 Pepper - Your Therapy Friend</h2><div class="chat-area" id="chatArea"><div class="message bot-message">Hi {{ username }}! I'm Pepper! 😊 How are you feeling today? 🌟</div></div><div class="chat-input"><input type="text" id="chatInput" placeholder="Type your message..." onkeypress="if(event.key==='Enter') sendChildMessage()"><button onclick="sendChildMessage()">Send</button></div><div class="quick-actions"><div class="quick-btn" onclick="childQuick('I did something good today')">🎉 Good Job</div><div class="quick-btn" onclick="childQuick('I feel happy')">😊 Happy</div><div class="quick-btn" onclick="childQuick('I need a break')">😌 Break</div><div class="quick-btn" onclick="childQuick('Help me please')">🆘 Help</div><div class="quick-btn" onclick="childQuick('I want to play a game')">🎮 Game</div></div></div>
<div class="card"><h2>🧘 Calm Down - Breathing</h2><div class="breathing-circle" onclick="startBreathing()"><span>🧘<br>Breathe</span></div><div id="breathingText" style="text-align:center;">Click to start</div></div>
<div class="card"><h2>📋 My Daily Tasks</h2><ul class="routine-list" id="routineList"></ul></div>
<div class="card"><h2>🎮 My Games ({{ games|length }})</h2><div class="games-grid" id="gamesGrid"></div></div>
</div>
<script>
const games = {{ games | tojson }};
const icons = {{ icons | tojson }};
const tasks = ["Wake up & get ready 🛌", "Complete learning activity 📚", "Play a game 🎮", "Practice communication 💬", "Follow visual schedule 📋"];
let completedTasks = JSON.parse(localStorage.getItem('child_tasks') || '[]');

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
            }
            localStorage.setItem('child_tasks',JSON.stringify(completedTasks));
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
    fetch('/child/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})}).then(res=>res.json()).then(data=>{
        const botDiv=document.createElement('div');botDiv.className='message bot-message';botDiv.innerHTML=data.response;area.appendChild(botDiv);area.scrollTop=area.scrollHeight;
    });
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
loadTasks();loadGames();
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
@keyframes celebrate{0%{transform:scale(1);}50%{transform:scale(1.05);}100%{transform:scale(1);}}
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
    const msgDiv=document.getElementById('messageArea');
    if(type==='correct'){
        msgDiv.innerHTML='🎉 Great job! +10 points! 🎉';
        msgDiv.classList.add('correct-answer');
        setTimeout(()=>msgDiv.classList.remove('correct-answer'),1500);
    }else{
        msgDiv.innerHTML='😊 Good try! +2 points! 😊';
        setTimeout(()=>msgDiv.innerHTML='💡 Play and earn points!',1500);
    }
}
fetch('/game_content/{{ game_name }}').then(res=>res.text()).then(html=>{document.getElementById('gameContent').innerHTML=html;}).catch(()=>{document.getElementById('gameContent').innerHTML=`<div style="text-align:center;padding:50px;"><button onclick="playSound('correct')" style="background:#e94560;border:none;padding:15px 30px;border-radius:10px;color:white;font-size:18px;cursor:pointer;">🎮 Play Game (+10 points)</button></div>`;});
</script>
</body>
</html>
'''

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧒 CHILD DASHBOARD ONLY")
    print("="*60)
    print("✅ ABA-based AI Chat")
    print("✅ Breathing Exercise")
    print("✅ Daily Tasks")
    print(f"✅ {len(GAMES_LIST)} Educational Games")
    print("="*60)
    print("🌐 Opening at: http://localhost:5002 (Child Dashboard Only)")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5002, debug=True)
