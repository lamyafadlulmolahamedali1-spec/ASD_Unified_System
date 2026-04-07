import os
import re

games_dir = "templates/games"
exclude = {'landing', 'parent_login', 'parent_register', 'child_login', 'games_menu', 'parent_dashboard'}
GAMES_LIST = []
if os.path.exists(games_dir):
    for f in os.listdir(games_dir):
        if f.endswith('.html') and os.path.splitext(f)[0] not in exclude:
            GAMES_LIST.append(os.path.splitext(f)[0])
GAMES_LIST.sort()

print(f"📋 قائمة الألعاب ({len(GAMES_LIST)}):")
for g in GAMES_LIST[:20]:
    print(f"   - {g}")

# إنشاء ICONS
ICONS = {
    'emotion_match': '😊', 'color_sort': '🎨', 'counting': '🔢', 'memory_game': '🧠',
    'aba_matching': '🎯', 'aba_sorting': '📊', 'alphabet_song': '🎵', 'animal_sounds': '🐶',
    'ball_sort_perfect': '⚾', 'block_blast': '🧩', 'brain_oddone': '🤔', 'brain_pattern': '🔄',
    'color_match': '🎨', 'coloring_game': '🖍️', 'crossword_english': '📝', 'daily_routine': '⏰',
    'do_dont': '✅', 'drawing_pad': '✏️', 'familiar_things': '🏠', 'language_game': '💬',
    'letter_coloring': '🔤', 'math_challenge': '🔢', 'memory_cards': '🎴', 'music_rhythm': '🎵',
    'pepper_emotions': '😊', 'pepper_imitation': '🤖', 'physical_activity': '🏃', 'sensory_bubbles': '🫧',
    'sensory_fireworks': '🎆', 'sensory_spinner': '🌀', 'shape_sorting': '⭐', 'smart_alarm': '⏰',
    'snake_game': '🐍', 'social_stories_english': '📖', 'spot_difference': '🔍', 'story_library_full': '📚',
    'sudoku': '🔢', 'teacch_schedule': '📋', 'teacch_work': '⚙️', 'tictactoe_game': '❌',
    'word_search': '🔍', 'work_system': '🔧'
}

# تحديث app.py
with open("app.py", "r") as f:
    content = f.read()

# استبدال GAMES_LIST
pattern = r"GAMES_LIST = \[.*?\]"
new_games = f"GAMES_LIST = {GAMES_LIST}"
content = re.sub(pattern, new_games, content, flags=re.DOTALL)

# استبدال ICONS
pattern = r"ICONS = \{.*?\}"
new_icons = f"ICONS = {ICONS}"
content = re.sub(pattern, new_icons, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)

print(f"✅ تم تحديث app.py بعدد {len(GAMES_LIST)} لعبة")
