from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

ALL_GAMES = [
    'aba_matching', 'aba_sorting', 'alphabet_song', 'animal_sounds',
    'ball_sort_perfect', 'block_blast', 'brain_oddone', 'brain_pattern',
    'color_match', 'coloring_game', 'crossword_english', 'daily_routine',
    'do_dont', 'drawing_pad', 'familiar_things', 'language_game',
    'letter_coloring', 'math_challenge', 'memory_cards', 'music_rhythm',
    'pepper_emotions', 'pepper_imitation', 'physical_activity', 'sensory_bubbles',
    'sensory_fireworks', 'sensory_spinner', 'shape_sorting', 'smart_alarm',
    'snake_game', 'social_stories_english', 'spot_difference', 'story_library_full',
    'sudoku', 'teacch_schedule', 'teacch_work', 'tictactoe_game', 'word_search',
    'work_system',
    'ai_chat', 'speech_game', 'emotion_game', 'routine_builder',
    'brain_engage', 'games4autism', 'autism_talk', 'cognibuddy',
    'littlestars', 'doodlebop', 'spectrumcare', 'autimate', 'otidom',
    'speech_pronunciation'
]

ICONS = {
    'aba_matching': '🎯', 'aba_sorting': '📊', 'alphabet_song': '🎵', 'animal_sounds': '🐶',
    'ball_sort_perfect': '⚾', 'block_blast': '🧩', 'brain_oddone': '🤔', 'brain_pattern': '🔄',
    'color_match': '🎨', 'coloring_game': '🖍️', 'crossword_english': '📝', 'daily_routine': '⏰',
    'do_dont': '✅', 'drawing_pad': '✏️', 'familiar_things': '🏠', 'language_game': '💬',
    'letter_coloring': '🔤', 'math_challenge': '🔢', 'memory_cards': '🎴', 'music_rhythm': '🎵',
    'pepper_emotions': '😊', 'pepper_imitation': '🤖', 'physical_activity': '🏃', 'sensory_bubbles': '🫧',
    'sensory_fireworks': '🎆', 'sensory_spinner': '🌀', 'shape_sorting': '⭐', 'smart_alarm': '⏰',
    'snake_game': '🐍', 'social_stories_english': '📖', 'spot_difference': '🔍', 'story_library_full': '📚',
    'sudoku': '🔢', 'teacch_schedule': '📋', 'teacch_work': '⚙️', 'tictactoe_game': '❌',
    'word_search': '🔍', 'work_system': '🔧',
    'ai_chat': '🤖', 'speech_game': '🎤', 'emotion_game': '😊', 'routine_builder': '📅',
    'brain_engage': '🧠', 'games4autism': '🎨', 'autism_talk': '💬', 'cognibuddy': '🧩',
    'littlestars': '⭐', 'doodlebop': '✏️', 'spectrumcare': '📊', 'autimate': '📋', 'otidom': '🎵',
    'speech_pronunciation': '🗣️'
}

@app.route('/')
def index():
    return render_template('games_list.html', games=ALL_GAMES, icons=ICONS)

@app.route('/game/<name>')
def play_game(name):
    if name in ALL_GAMES:
        return render_template(f'{name}.html')
    return "Game not found", 404

@app.route('/progress')
def progress():
    return render_template('progress.html')

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎮 PEPPER THERAPY - ALL GAMES WORKING")
    print("="*60)
    print(f"📍 http://localhost:5009")
    print(f"📍 Total Games: {len(ALL_GAMES)}")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5009)
