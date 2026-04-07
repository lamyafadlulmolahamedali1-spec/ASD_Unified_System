// Auto Tracker - Automatically detects and tracks correct/wrong answers
(function() {
    // Wait for page to load
    setTimeout(() => {
        if (typeof stats === 'undefined') return;
        
        console.log('🎯 Auto Tracker activated');
        
        // 1. Track button clicks - if button has correct/wrong class
        document.querySelectorAll('button, .option, .choice, .item-card, .card, .answer-btn, .quiz-option').forEach(btn => {
            const originalClick = btn.onclick;
            btn.addEventListener('click', function(e) {
                // Check if this is a correct answer
                if (btn.classList.contains('correct') || 
                    btn.classList.contains('right') ||
                    btn.getAttribute('data-correct') === 'true' ||
                    btn.innerHTML.includes('✅') ||
                    btn.innerHTML.includes('Correct')) {
                    stats.addCorrect();
                }
                // Check if this is a wrong answer
                else if (btn.classList.contains('wrong') || 
                         btn.classList.contains('incorrect') ||
                         btn.getAttribute('data-wrong') === 'true' ||
                         btn.innerHTML.includes('❌') ||
                         btn.innerHTML.includes('Wrong')) {
                    stats.addWrong();
                }
            });
        });
        
        // 2. Track form submissions
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function(e) {
                const input = form.querySelector('input');
                if (input && input.value) {
                    // Auto-detect if answer is correct (you can customize)
                    setTimeout(() => {
                        stats.addCorrect();
                    }, 100);
                }
            });
        });
        
        // 3. Track correct/wrong messages in feedback
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    const feedback = document.getElementById('feedback') || 
                                    document.querySelector('.message') ||
                                    document.querySelector('.feedback');
                    if (feedback && feedback.innerHTML) {
                        const text = feedback.innerHTML.toLowerCase();
                        if (text.includes('correct') || text.includes('right') || text.includes('good')) {
                            stats.addCorrect();
                        } else if (text.includes('wrong') || text.includes('incorrect') || text.includes('try again')) {
                            stats.addWrong();
                        }
                    }
                }
            });
        });
        
        const feedbackElement = document.getElementById('feedback') || document.querySelector('.message');
        if (feedbackElement) {
            observer.observe(feedbackElement, { childList: true, subtree: true, characterData: true });
        }
    }, 1000);
})();
