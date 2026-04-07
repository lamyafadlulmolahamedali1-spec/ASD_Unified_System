#!/usr/bin/env python3
"""
ASD Dashboard Enhanced - متكامل مع:
- Autism Support Chatbot (للآباء)
- Emotion Recognition
- Daily Routine Manager
- Breathing Exercise
- Therapy Recommendations
- Progress Tracking
- Games Dashboard
"""

from flask import Flask, render_template_string, request, jsonify
import json
import time
import random
from datetime import datetime
import os

app = Flask(__name__)

# ========== Autism Knowledge Base (لإجابة أسئلة الآباء) ==========
AUTISM_KNOWLEDGE = {
    # أساسيات التوحد
    "what is autism": "Autism Spectrum Disorder (ASD) is a developmental condition that affects how a person communicates, interacts with others, and experiences the world. Every person with autism is unique with their own strengths and challenges.",
    
    "signs of autism": "Common early signs include: delayed speech, avoiding eye contact, not responding to name, repetitive movements (hand flapping, rocking), sensory sensitivities (lights, sounds, textures), and difficulty with social interactions.",
    
    "causes of autism": "Autism is believed to be caused by a combination of genetic and environmental factors. There is no single cause, and vaccines do NOT cause autism.",
    
    # العلاجات
    "aba therapy": "ABA (Applied Behavior Analysis) is an evidence-based therapy that uses positive reinforcement to teach new skills and reduce challenging behaviors. It's considered the gold standard for autism intervention.",
    
    "speech therapy": "Speech therapy helps with communication skills, including verbal and non-verbal communication. It can help with articulation, social language, and alternative communication methods like PECS or AAC devices.",
    
    "occupational therapy": "Occupational therapy (OT) helps with sensory processing, fine motor skills, daily living skills (dressing, eating), and self-regulation. It's very important for children with autism.",
    
    # التواصل
    "how to communicate": "Use simple, clear language. Give extra time to process. Use visual supports (pictures, PECS). Be patient and listen actively. Validate their feelings and communication attempts.",
    
    "pecs": "PECS (Picture Exchange Communication System) is a visual communication system where the child exchanges pictures to communicate needs, wants, and thoughts. It's very effective for non-verbal children.",
    
    # السلوك
    "meltdown vs tantrum": "A meltdown is an involuntary reaction to sensory overload or stress - the child cannot control it. A tantrum is goal-oriented and stops when the goal is met. Meltdowns require safety and calm; tantrums need boundaries.",
    
    "how to handle meltdown": "Stay calm. Reduce sensory input (lights, sounds, people). Ensure safety. Don't argue or punish. Give space and time to recover. Afterward, talk about what happened and coping strategies.",
    
    "sensory overload": "Sensory overload happens when the brain receives more input than it can process. Signs: covering ears, hiding, crying, aggression. Help by: reducing stimuli, moving to a quiet space, offering deep pressure, using noise-canceling headphones.",
    
    # الروتين
    "routine importance": "Routines provide predictability and reduce anxiety. Use visual schedules. Warn before transitions. Keep consistent daily patterns for meals, sleep, and activities.",
    
    "visual schedule": "Visual schedules use pictures or words to show what will happen. They help with transitions and reduce anxiety. Place them at eye level and review them together.",
    
    # الأهل
    "parent support": "Take care of yourself too! Join support groups, seek respite care, connect with other parents, and remember you're not alone. Your well-being matters.",
    
    "early intervention": "Early intervention (before age 3) greatly improves outcomes. Seek evaluation if concerned. Services may include speech, OT, ABA, and developmental therapy.",
    
    "school preparation": "Visit the school beforehand. Create a one-page profile about your child. Meet with teachers and support staff. Practice routines at home. Use social stories.",
}

# ========== Daily Routines ==========
DAILY_ROUTINES = {
    "morning": [
        {"task": "Wake up", "time": "7:00 AM", "completed": False},
        {"task": "Brush teeth", "time": "7:15 AM", "completed": False},
        {"task": "Wash face", "time": "7:20 AM", "completed": False},
        {"task": "Get dressed", "time": "7:30 AM", "completed": False},
        {"task": "Eat breakfast", "time": "7:45 AM", "completed": False},
        {"task": "Pack bag", "time": "8:00 AM", "completed": False}
    ],
    "afternoon": [
        {"task": "Learning time", "time": "10:00 AM", "completed": False},
        {"task": "Play time", "time": "11:30 AM", "completed": False},
        {"task": "Eat lunch", "time": "12:30 PM", "completed": False},
        {"task": "Rest time", "time": "1:30 PM", "completed": False},
        {"task": "Outdoor walk", "time": "3:00 PM", "completed": False}
    ],
    "evening": [
        {"task": "Eat dinner", "time": "6:00 PM", "completed": False},
        {"task": "Bath time", "time": "7:00 PM", "completed": False},
        {"task": "Read story", "time": "7:45 PM", "completed": False},
        {"task": "Brush teeth", "time": "8:00 PM", "completed": False},
        {"task": "Bedtime", "time": "8:30 PM", "completed": False}
    ]
}

# ========== Breathing Exercises ==========
BREATHING_EXERCISES = {
    "4-4-4": {"in": 4, "hold": 4, "out": 4, "name": "Calming Breath"},
    "4-7-8": {"in": 4, "hold": 7, "out": 8, "name": "Relaxing Breath"},
    "square": {"in": 4, "hold": 4, "out": 4, "hold2": 4, "name": "Square Breathing"}
}

# ========== Therapy Recommendations ==========
THERAPY_TIPS = {
    "aba": "ABA uses positive reinforcement. Break tasks into small steps. Use consistent prompts and fading. Track progress daily.",
    "speech": "Model language. Use parallel talk (describe what child is doing). Expand their words. Use visual supports.",
    "ot": "Create a sensory diet. Offer movement breaks. Use weighted blankets. Provide fidget toys.",
    "social": "Use social stories. Practice turn-taking. Model appropriate interactions. Praise social attempts."
}

# ========== HTML Template ==========
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASD Support Dashboard - Pepper</title>
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
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        @media (max-width: 768px) { .dashboard { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧩 ASD Support Dashboard - Pepper Robot</h1>
        <p>Support for Parents & Children | ABA | TEACCH | PECS | Sensory Support</p>
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
        
        <!-- Card 4: Parent Dashboard - Progress -->
        <div class="card">
            <h2>📊 Progress Dashboard</h2>
            <div class="stat">
                <span>📅 Sessions this week:</span>
                <span class="stat-value" id="sessionCount">0</span>
            </div>
            <div class="stat">
                <span>💬 Questions asked:</span>
                <span class="stat-value" id="questionCount">0</span>
            </div>
            <div class="stat">
                <span>✅ Tasks completed:</span>
                <span class="stat-value" id="completedCount">0</span>
            </div>
            <div class="stat">
                <span>🧘 Breathing exercises:</span>
                <span class="stat-value" id="breathingCount">0</span>
            </div>
            <div class="quick-actions">
                <button class="quick-btn" onclick="generateReport()">📄 Generate Report</button>
                <button class="quick-btn" onclick="resetStats()">🔄 Reset Stats</button>
            </div>
            <div id="reportArea" style="margin-top: 15px; font-size: 12px; color: #ccc;"></div>
        </div>
    </div>
    
    <script>
        // Knowledge base for chatbot
        const knowledgeBase = {
            "what is autism": "Autism Spectrum Disorder (ASD) is a developmental condition that affects communication, behavior, and social interaction. Each person with autism is unique with their own strengths and challenges.",
            "signs of autism": "Common early signs include: delayed speech, avoiding eye contact, not responding to name, repetitive movements, sensory sensitivities, and difficulty with social interactions.",
            "aba therapy": "ABA (Applied Behavior Analysis) uses positive reinforcement to teach new skills and reduce challenging behaviors. It's evidence-based and considered the gold standard.",
            "speech therapy": "Speech therapy helps with communication skills, including verbal and non-verbal communication, articulation, and social language.",
            "occupational therapy": "Occupational therapy (OT) helps with sensory processing, fine motor skills, daily living skills, and self-regulation.",
            "how to handle meltdown": "Stay calm. Reduce sensory input. Ensure safety. Don't argue or punish. Give space and time to recover.",
            "sensory overload": "Signs include covering ears, hiding, crying, aggression. Help by reducing stimuli, moving to a quiet space, offering deep pressure, using noise-canceling headphones.",
            "routine importance": "Routines provide predictability and reduce anxiety. Use visual schedules. Warn before transitions. Keep consistent daily patterns.",
            "how to communicate": "Use simple, clear language. Give extra time to process. Use visual supports. Be patient and listen actively.",
            "early intervention": "Early intervention (before age 3) greatly improves outcomes. Seek evaluation if concerned. Services may include speech, OT, ABA, and developmental therapy."
        };
        
        let sessionCount = localStorage.getItem("sessionCount") ? parseInt(localStorage.getItem("sessionCount")) : 0;
        let questionCount = localStorage.getItem("questionCount") ? parseInt(localStorage.getItem("questionCount")) : 0;
        let breathingCount = localStorage.getItem("breathingCount") ? parseInt(localStorage.getItem("breathingCount")) : 0;
        let completedTasks = localStorage.getItem("completedTasks") ? JSON.parse(localStorage.getItem("completedTasks")) : [];
        
        let currentRoutine = "morning";
        let routines = {
            morning: [
                "Wake up 🛌", "Brush teeth 🪥", "Wash face 🧼", "Get dressed 👕", "Eat breakfast 🍳", "Pack bag 🎒"
            ],
            afternoon: [
                "Learning time 📚", "Play time 🎮", "Eat lunch 🍎", "Rest time 😴", "Outdoor walk 🚶"
            ],
            evening: [
                "Eat dinner 🍽️", "Bath time 🛁", "Read story 📖", "Brush teeth 🪥", "Bedtime 😴"
            ]
        };
        
        sessionCount++;
        localStorage.setItem("sessionCount", sessionCount);
        
        function updateStats() {
            document.getElementById("sessionCount").innerText = sessionCount;
            document.getElementById("questionCount").innerText = questionCount;
            document.getElementById("breathingCount").innerText = breathingCount;
            document.getElementById("completedCount").innerText = completedTasks.length;
        }
        
        function sendMessage() {
            const input = document.getElementById("chatInput");
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, "user");
            input.value = "";
            questionCount++;
            updateStats();
            localStorage.setItem("questionCount", questionCount);
            
            let response = getResponse(message);
            setTimeout(() => addMessage(response, "bot"), 500);
        }
        
        function getResponse(question) {
            const q = question.toLowerCase();
            for (let [key, answer] of Object.entries(knowledgeBase)) {
                if (q.includes(key)) {
                    return answer;
                }
            }
            return "I'm here to help! You can ask me about autism signs, therapies, sensory overload, communication tips, routines, and more. What would you like to know?";
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
            updateStats();
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
        
        function generateReport() {
            const report = `
📊 WEEKLY REPORT 📊
===================
📅 Sessions: ${sessionCount}
💬 Questions: ${questionCount}
✅ Tasks completed: ${completedTasks.length}
🧘 Breathing exercises: ${breathingCount}
===================
Keep up the great work! 🌟
            `;
            document.getElementById("reportArea").innerHTML = report.replace(/\n/g, "<br>");
            addMessage("Here's your weekly progress report! Check the Parent Dashboard card. 📊", "bot");
        }
        
        function resetStats() {
            sessionCount = 0;
            questionCount = 0;
            breathingCount = 0;
            completedTasks = [];
            localStorage.setItem("sessionCount", sessionCount);
            localStorage.setItem("questionCount", questionCount);
            localStorage.setItem("breathingCount", breathingCount);
            localStorage.setItem("completedTasks", JSON.stringify(completedTasks));
            updateStats();
            updateRoutineList();
            addMessage("Stats have been reset. Ready for a fresh start! 🌟", "bot");
        }
        
        updateStats();
        updateRoutineList();
    </script>
</body>
</html>
'''

# ========== Flask Routes ==========
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '').lower()
    
    for key, answer in AUTISM_KNOWLEDGE.items():
        if key in question:
            return jsonify({'response': answer})
    
    return jsonify({'response': "I'm here to help! Ask me about autism signs, therapies, communication, sensory needs, or daily routines."})

@app.route('/routine/<time_of_day>', methods=['GET'])
def get_routine(time_of_day):
    return jsonify(DAILY_ROUTINES.get(time_of_day, DAILY_ROUTINES['morning']))

@app.route('/complete_task', methods=['POST'])
def complete_task():
    data = request.json
    task = data.get('task')
    return jsonify({'status': 'success', 'message': f'Completed: {task}'})

@app.route('/breathing/<exercise_type>', methods=['GET'])
def get_breathing(exercise_type):
    return jsonify(BREATHING_EXERCISES.get(exercise_type, BREATHING_EXERCISES['4-4-4']))

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧩 ASD ENHANCED DASHBOARD")
    print("="*50)
    print("🌐 Opening at: http://localhost:5001")
    print("📚 Autism Knowledge Base loaded")
    print("✅ Daily routines loaded")
    print("✅ Breathing exercises loaded")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
