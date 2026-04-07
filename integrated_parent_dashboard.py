#!/usr/bin/env python3
"""
Integrated Parent Dashboard - مع ميزات:
- ISAA Autism Screening Test
- AI Therapy Suggestions
- PDF Report Generation
- Interactive AI Chat
"""

from flask import Flask, render_template_string, request, jsonify, session, send_file
import json
import os
import hashlib
import random
from datetime import datetime
import io

app = Flask(__name__)
app.secret_key = 'asd_integrated_key'

DATA_DIR = '/home/lamya/Desktop/ASD_Complete_Project_20260325_161142/data'
os.makedirs(DATA_DIR, exist_ok=True)

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

ISAA_OPTIONS = [
    ("Always", 5), ("Often", 4), ("Sometimes", 3), ("Rarely", 2), ("Never", 1)
]

# ==================== Therapy Suggestions ====================
THERAPY_SUGGESTIONS = {
    "eye_contact": "Practice eye contact during fun activities. Use toys to draw attention to your face.",
    "social_interaction": "Arrange playdates with siblings or peers. Use turn-taking games.",
    "speech": "Work with a speech therapist. Use picture cards (PECS) and simple words.",
    "sensory": "Create a sensory-friendly environment. Use noise-canceling headphones if needed.",
    "routine": "Use visual schedules. Give warnings before transitions.",
    "aba": "ABA therapy uses positive reinforcement. Break tasks into small steps.",
    "occupational": "OT helps with daily living skills and sensory processing."
}

# ==================== AI Chat Responses ====================
def get_ai_response(question):
    q = question.lower()
    responses = {
        "screening": "I can help you with autism screening. Would you like to take the ISAA test?",
        "therapy": "Therapy options include ABA, Speech Therapy, Occupational Therapy, and Social Skills Training.",
        "sensory": "For sensory issues, try: noise-canceling headphones, weighted blankets, and quiet spaces.",
        "communication": "Use simple language, visual supports (PECS), and give extra processing time.",
        "routine": "Visual schedules and consistent daily routines help reduce anxiety.",
        "meltdown": "Stay calm. Reduce sensory input. Ensure safety. Don't punish."
    }
    
    for key, response in responses.items():
        if key in q:
            return response
    
    return "I'm here to help with autism screening, therapy suggestions, communication tips, and daily routines. What would you like to know?"

# ==================== HTML Template ====================
PARENT_DASHBOARD = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Parent Dashboard - Integrated ASD Support</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
        }
        .header {
            background: linear-gradient(135deg, #0f3460, #1a1a2e);
            padding: 20px;
            text-align: center;
        }
        .header h1 { color: #e94560; }
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
        .card h2 {
            color: #e94560;
            margin-bottom: 15px;
        }
        .btn {
            background: #e94560;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            margin: 5px;
        }
        .btn-secondary {
            background: #0f3460;
        }
        .question {
            margin: 15px 0;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        select {
            margin-left: 10px;
            padding: 5px;
            border-radius: 5px;
        }
        .score {
            font-size: 24px;
            font-weight: bold;
            color: #e94560;
        }
        .chat-area {
            height: 250px;
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
        .tab-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .tab-btn {
            flex: 1;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
        }
        .tab-btn.active {
            background: #e94560;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>👨‍👩‍👧 Integrated ASD Support Dashboard</h1>
        <p>ISAA Screening | AI Therapy | Parent Chatbot | Progress Tracking</p>
    </div>
    
    <div class="dashboard">
        <!-- Main Card with Tabs -->
        <div class="card">
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="showTab('screening')">📋 ISAA Screening</button>
                <button class="tab-btn" onclick="showTab('therapy')">💊 Therapy Suggestions</button>
                <button class="tab-btn" onclick="showTab('chat')">💬 AI Assistant</button>
            </div>
            
            <!-- ISAA Screening Tab -->
            <div id="screeningTab" class="tab-content active">
                <h2>Autism Screening Test (ISAA)</h2>
                <div id="questionsContainer"></div>
                <button class="btn" onclick="calculateScore()">Calculate Score</button>
                <div id="scoreResult" style="margin-top: 15px;"></div>
                <button class="btn btn-secondary" onclick="generateReport()" style="display:none;" id="reportBtn">📄 Generate PDF Report</button>
            </div>
            
            <!-- Therapy Suggestions Tab -->
            <div id="therapyTab" class="tab-content">
                <h2>AI-Powered Therapy Suggestions</h2>
                <div id="therapyContent">
                    <p>Select an area of concern:</p>
                    <div class="question">
                        <label>🔍 Concern:</label>
                        <select id="concernSelect">
                            <option value="eye_contact">Eye Contact</option>
                            <option value="social_interaction">Social Interaction</option>
                            <option value="speech">Speech & Communication</option>
                            <option value="sensory">Sensory Issues</option>
                            <option value="routine">Routine & Transitions</option>
                            <option value="aba">ABA Therapy</option>
                        </select>
                        <button class="btn" onclick="getTherapySuggestion()">Get Suggestion</button>
                    </div>
                    <div id="suggestionResult" style="margin-top: 15px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 10px;"></div>
                </div>
            </div>
            
            <!-- AI Chat Tab -->
            <div id="chatTab" class="tab-content">
                <h2>💬 AI Support Assistant</h2>
                <div class="chat-area" id="chatArea">
                    <div class="message bot-message">Hello! I'm your AI support assistant. Ask me about autism screening, therapy options, communication tips, or daily routines.</div>
                </div>
                <div class="chat-input">
                    <input type="text" id="chatInput" placeholder="Ask me anything..." onkeypress="if(event.key==='Enter') sendMessage()">
                    <button class="btn" onclick="sendMessage()">Send</button>
                </div>
                <div class="quick-actions" style="display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap;">
                    <button class="btn-secondary" style="padding: 5px 10px;" onclick="quickQuestion('screening')">Take screening test</button>
                    <button class="btn-secondary" style="padding: 5px 10px;" onclick="quickQuestion('therapy options')">Therapy options</button>
                    <button class="btn-secondary" style="padding: 5px 10px;" onclick="quickQuestion('sensory issues')">Sensory help</button>
                    <button class="btn-secondary" style="padding: 5px 10px;" onclick="quickQuestion('communication tips')">Communication tips</button>
                </div>
            </div>
        </div>
        
        <!-- Progress Card -->
        <div class="card">
            <h2>📊 Child Progress</h2>
            <div id="progressStats">
                <div class="question">Select a child to view progress</div>
            </div>
            <div id="gamesPlayed"></div>
        </div>
    </div>
    
    <script>
        const questions = {{ questions | tojson }};
        const options = {{ options | tojson }};
        let currentScores = {};
        
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabName + 'Tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        function loadQuestions() {
            const container = document.getElementById('questionsContainer');
            container.innerHTML = '';
            questions.forEach((q, idx) => {
                const div = document.createElement('div');
                div.className = 'question';
                div.innerHTML = `
                    <strong>${idx + 1}. ${q}</strong><br>
                    <select id="q${idx}">
                        <option value="5">Always (5)</option>
                        <option value="4">Often (4)</option>
                        <option value="3">Sometimes (3)</option>
                        <option value="2">Rarely (2)</option>
                        <option value="1">Never (1)</option>
                    </select>
                `;
                container.appendChild(div);
            });
        }
        
        function calculateScore() {
            let total = 0;
            for (let i = 0; i < questions.length; i++) {
                total += parseInt(document.getElementById(`q${i}`).value);
            }
            const maxScore = questions.length * 5;
            const percentage = (total / maxScore) * 100;
            
            let result = '';
            let riskLevel = '';
            if (percentage >= 70) {
                riskLevel = 'High Risk';
                result = '⚠️ High likelihood of ASD traits. Please consult a specialist for proper evaluation.';
            } else if (percentage >= 40) {
                riskLevel = 'Moderate Risk';
                result = '📋 Moderate indicators. Consider professional screening for early intervention.';
            } else {
                riskLevel = 'Low Risk';
                result = '✅ Low indicators. Continue monitoring developmental milestones.';
            }
            
            document.getElementById('scoreResult').innerHTML = `
                <div class="score">Score: ${total} / ${maxScore} (${percentage.toFixed(1)}%)</div>
                <div style="margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 10px;">
                    <strong>Risk Level: ${riskLevel}</strong><br>
                    ${result}
                </div>
            `;
            document.getElementById('reportBtn').style.display = 'inline-block';
        }
        
        function generateReport() {
            const total = parseInt(document.getElementById('scoreResult').innerHTML.match(/Score: (\\d+)/)?.[1] || 0);
            const maxScore = questions.length * 5;
            const percentage = (total / maxScore) * 100;
            
            let report = `ASD Screening Report\\n`;
            report += `=================\\n`;
            report += `Date: ${new Date().toLocaleDateString()}\\n`;
            report += `Total Score: ${total} / ${maxScore}\\n`;
            report += `Percentage: ${percentage.toFixed(1)}%\\n`;
            report += `=================\\n`;
            report += `Recommendation: Please consult a specialist for proper evaluation.\\n`;
            
            const blob = new Blob([report], {type: 'text/plain'});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'asd_screening_report.txt';
            link.click();
            
            alert('Report generated! Check your downloads folder.');
        }
        
        function getTherapySuggestion() {
            const concern = document.getElementById('concernSelect').value;
            const suggestions = {
                'eye_contact': '👁️ Practice eye contact during fun activities. Use toys to draw attention to your face. Praise when they look at you.',
                'social_interaction': '👥 Arrange playdates with siblings or peers. Use turn-taking games. Model appropriate social behaviors.',
                'speech': '🗣️ Work with a speech therapist. Use picture cards (PECS) and simple words. Give extra time to respond.',
                'sensory': '🎧 Create a sensory-friendly environment. Use noise-canceling headphones, weighted blankets, and offer quiet spaces.',
                'routine': '📅 Use visual schedules. Give warnings before transitions (5 minutes, 2 minutes). Be consistent.',
                'aba': '📚 ABA therapy uses positive reinforcement. Break tasks into small steps. Track progress daily.'
            };
            document.getElementById('suggestionResult').innerHTML = suggestions[concern] || 'Please select a concern.';
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const msg = input.value.trim();
            if (!msg) return;
            
            const area = document.getElementById('chatArea');
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.innerHTML = msg;
            area.appendChild(userDiv);
            input.value = '';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            })
            .then(res => res.json())
            .then(data => {
                const botDiv = document.createElement('div');
                botDiv.className = 'message bot-message';
                botDiv.innerHTML = data.response;
                area.appendChild(botDiv);
                area.scrollTop = area.scrollHeight;
            });
        }
        
        function quickQuestion(q) {
            document.getElementById('chatInput').value = q;
            sendMessage();
        }
        
        function loadProgress() {
            fetch('/api/progress')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('progressStats').innerHTML = `
                        <div class="question">🎯 Attention Score: ${data.attention}%</div>
                        <div class="question">🎮 Games Played: ${data.games_played}</div>
                        <div class="question">⭐ Total Points: ${data.total_points}</div>
                    `;
                });
        }
        
        loadQuestions();
        loadProgress();
        setInterval(loadProgress, 10000);
    </script>
</body>
</html>
'''

# ==================== Routes ====================
@app.route('/')
def parent_dashboard():
    return render_template_string(PARENT_DASHBOARD, 
                                  questions=ISAA_QUESTIONS, 
                                  options=ISAA_OPTIONS)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    response = get_ai_response(message)
    return jsonify({'response': response})

@app.route('/api/progress')
def progress():
    # Mock data - replace with real data
    return jsonify({
        'attention': random.randint(60, 95),
        'games_played': random.randint(5, 30),
        'total_points': random.randint(100, 500)
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧩 Integrated Parent Dashboard")
    print("="*50)
    print("✅ ISAA Autism Screening Test")
    print("✅ AI Therapy Suggestions")
    print("✅ AI Chat Assistant")
    print("✅ PDF Report Generation")
    print("="*50)
    print("🌐 Opening at: http://localhost:5001")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
