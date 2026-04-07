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

# تحديث app.py
with open("app.py", "r") as f:
    content = f.read()

# استبدال GAMES_LIST
pattern = r"GAMES_LIST = \[.*?\]"
new_games = f"GAMES_LIST = {GAMES_LIST}"
content = re.sub(pattern, new_games, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)

print(f"✅ تم تحديث app.py بعدد {len(GAMES_LIST)} لعبة")
print(f"📋 الألعاب: {GAMES_LIST[:10]}...")
