import os
import re

# قراءة قائمة الألعاب من مجلد Pepper_Therapy
games_dir = "/home/lamya/Desktop/Pepper_Therapy_Final_20260330/templates/games"
if os.path.exists(games_dir):
    games = [f.replace('.html', '') for f in os.listdir(games_dir) if f.endswith('.html')]
    games.sort()
else:
    # إذا لم يكن المجلد موجوداً، استخدم القائمة الافتراضية
    games = [
        'aba_matching', 'aba_sorting', 'alphabet_song', 'animal_sounds',
        'ball_sort_perfect', 'block_blast', 'brain_oddone', 'brain_pattern',
        'color_match', 'coloring_game', 'crossword_english', 'daily_routine',
        'do_dont', 'drawing_pad', 'emotion_match', 'familiar_things',
        'language_game', 'letter_coloring', 'math_challenge', 'memory_cards',
        'memory_game', 'music_rhythm', 'pepper_emotions', 'pepper_imitation',
        'physical_activity', 'sensory_bubbles', 'sensory_fireworks', 'sensory_spinner',
        'shape_sorting', 'smart_alarm', 'snake_game', 'social_stories_english',
        'spot_difference', 'story_library_full', 'sudoku', 'teacch_schedule',
        'teacch_work', 'tictactoe_game', 'word_search', 'work_system',
        'color_sort', 'counting', 'balloon_pop', 'memory_match', 'pattern_game',
        'number_sort', 'letter_trace', 'emotion_guess', 'social_scenario',
        'breathing_buddy', 'reward_chart', 'daily_journal', 'sensory_calming'
    ]

print(f"✅ عدد الألعاب الجديدة: {len(games)}")

# تحديث ملف final_complete_system.py
with open("final_complete_system.py", "r") as f:
    content = f.read()

# استبدال قائمة GAMES_LIST
pattern = r"GAMES_LIST = \[.*?\]"
new_games = f"GAMES_LIST = {games}"
content = re.sub(pattern, new_games, content, flags=re.DOTALL)

# تحديث أيقونات الألعاب
icons = {}
for game in games:
    # أيقونات افتراضية
    default_icons = {
        'balloon_pop': '🎈', 'memory_match': '🎴', 'pattern_game': '🔄',
        'number_sort': '🔢', 'letter_trace': '✏️', 'emotion_guess': '😊',
        'social_scenario': '👥', 'breathing_buddy': '🌬️', 'reward_chart': '🏆',
        'daily_journal': '📔', 'sensory_calming': '🧘', 'color_sort': '🎨',
        'counting': '🔢', 'emotion_match': '😊', 'memory_game': '🧠'
    }
    icons[game] = default_icons.get(game, '🎮')

# تحديث ICONS
icons_str = "ICONS = {\n"
for game, icon in icons.items():
    icons_str += f"    '{game}': '{icon}',\n"
icons_str += "}"

pattern_icons = r"ICONS = \{.*?\}"
content = re.sub(pattern_icons, icons_str, content, flags=re.DOTALL)

with open("final_complete_system.py", "w") as f:
    f.write(content)

print(f"✅ تم تحديث final_complete_system.py مع {len(games)} لعبة")
