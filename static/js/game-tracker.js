window.GameStats = class {
    constructor(gameName) {
        this.gameName = gameName;
        this.correct = 0;
        this.wrong = 0;
        this.score = 0;
    }
    addCorrect() {
        this.correct++;
        this.score += 10;
        this.save();
    }
    addWrong() {
        this.wrong++;
        this.save();
    }
    save() {
        fetch('/api/submit-score', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                child_name: 'lam',
                game_name: this.gameName,
                correct: this.correct,
                wrong: this.wrong,
                score: this.score
            })
        }).catch(e => console.error(e));
    }
};
