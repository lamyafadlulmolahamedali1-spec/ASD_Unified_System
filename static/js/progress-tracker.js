// Universal Progress Tracker for All Games
class GameTracker {
    constructor(gameId, childName = 'Player') {
        this.gameId = gameId;
        this.childName = childName;
        this.correct = 0;
        this.wrong = 0;
        this.score = 0;
        this.level = 1;
        this.startTime = Date.now();
        this.sessions = [];
    }
    
    // Call when answer is correct
    addCorrect(points = 10) {
        this.correct++;
        this.score += points;
        this.save();
        this.showFeedback('✅ Correct! +' + points + ' points', 'correct');
        this.updateDisplay();
    }
    
    // Call when answer is wrong
    addWrong() {
        this.wrong++;
        this.score = Math.max(0, this.score - 5);
        this.save();
        this.showFeedback('❌ Wrong! -5 points', 'wrong');
        this.updateDisplay();
    }
    
    // Call when level increases
    levelUp(newLevel) {
        this.level = newLevel;
        this.save();
        this.showCelebration();
        this.updateDisplay();
    }
    
    // Save progress to localStorage and server
    save() {
        const data = {
            gameId: this.gameId,
            childName: this.childName,
            correct: this.correct,
            wrong: this.wrong,
            score: this.score,
            level: this.level,
            timestamp: new Date().toISOString()
        };
        
        // Save to localStorage
        let allProgress = JSON.parse(localStorage.getItem('gameProgress') || '{}');
        if (!allProgress[this.gameId]) allProgress[this.gameId] = [];
        allProgress[this.gameId].push(data);
        localStorage.setItem('gameProgress', JSON.stringify(allProgress));
        
        // Save to server (if available)
        fetch('/api/progress/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).catch(e => console.log('Server save disabled'));
    }
    
    // Update display
    updateDisplay() {
        if (document.getElementById('score')) {
            document.getElementById('score').textContent = this.score;
        }
        if (document.getElementById('correct')) {
            document.getElementById('correct').textContent = this.correct;
        }
        if (document.getElementById('wrong')) {
            document.getElementById('wrong').textContent = this.wrong;
        }
        if (document.getElementById('level')) {
            document.getElementById('level').textContent = this.level;
        }
    }
    
    // Show feedback message
    showFeedback(message, type) {
        let feedbackDiv = document.getElementById('feedback');
        if (!feedbackDiv) {
            feedbackDiv = document.createElement('div');
            feedbackDiv.id = 'feedback';
            document.querySelector('.container').appendChild(feedbackDiv);
        }
        feedbackDiv.textContent = message;
        feedbackDiv.className = 'feedback ' + type;
        setTimeout(() => {
            feedbackDiv.textContent = '';
            feedbackDiv.className = '';
        }, 1500);
    }
    
    // Show celebration
    showCelebration() {
        const celebration = document.createElement('div');
        celebration.innerHTML = '🎉 LEVEL UP! 🎉';
        celebration.style.position = 'fixed';
        celebration.style.top = '50%';
        celebration.style.left = '50%';
        celebration.style.transform = 'translate(-50%, -50%)';
        celebration.style.fontSize = '3em';
        celebration.style.background = 'gold';
        celebration.style.padding = '20px 40px';
        celebration.style.borderRadius = '50px';
        celebration.style.zIndex = '1000';
        celebration.style.animation = 'celebrate 1s ease';
        document.body.appendChild(celebration);
        
        // Create confetti effect
        for (let i = 0; i < 30; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.textContent = '⭐';
                confetti.style.position = 'fixed';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.top = '-20px';
                confetti.style.fontSize = Math.random() * 20 + 10 + 'px';
                confetti.style.animation = 'fall 2s linear forwards';
                confetti.style.pointerEvents = 'none';
                document.body.appendChild(confetti);
                setTimeout(() => confetti.remove(), 2000);
            }, i * 100);
        }
        
        setTimeout(() => celebration.remove(), 2000);
    }
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fall {
        to { transform: translateY(100vh); opacity: 0; }
    }
    @keyframes celebrate {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.2); }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    }
    .feedback {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 1.2em;
        z-index: 1000;
        animation: slideUp 0.3s ease;
    }
    .feedback.correct {
        background: #d4edda;
        color: #155724;
        border: 2px solid #28a745;
    }
    .feedback.wrong {
        background: #f8d7da;
        color: #721c24;
        border: 2px solid #dc3545;
    }
    @keyframes slideUp {
        from { transform: translateX(-50%) translateY(100px); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
`;
document.head.appendChild(style);
