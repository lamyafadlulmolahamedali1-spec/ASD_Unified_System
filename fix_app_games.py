import os
import re

games_dir = "templates/games"
exclude = {'landing', 'parent_login', 'parent_register', 'child_login', 'games_menu', 'parent_dashboard', 'index'}

# جمع الألعاب من مجلد games فقط
GAMES_LIST = []
if os.path.exists(games_dir):
    for f in os.listdir(games_dir):
        if f.endswith('.html') and os.path.splitext(f)[0] not in exclude:
            GAMES_LIST.append(os.path.splitext(f)[0])
GAMES_LIST = list(set(GAMES_LIST))  # إزالة التكرار
GAMES_LIST.sort()

print(f"📋 عدد الألعاب الفعلية: {len(GAMES_LIST)}")
for g in GAMES_LIST[:15]:
    print(f"   - {g}")

# تحديث app.py
with open("app.py", "r") as f:
    content = f.read()

# استبدال GAMES_LIST
pattern = r"GAMES_LIST = \[.*?\]"
new_games = f"GAMES_LIST = {GAMES_LIST}"
content = re.sub(pattern, new_games, content, flags=re.DOTALL)

# إزالة أي مكان آخر يقرأ الألعاب من templates مباشرة
# تعديل دالة games_menu للتأكد
old_func = """@app.route('/games')
def games_menu():
    if 'user_type' not in session or session['user_type'] != 'child':
        return redirect(url_for('child_login'))
    return render_template('games_menu.html', games=GAMES_LIST, icons=ICONS, child_name=session['child_name'])"""

# تأكد من أنها تستخدم GAMES_LIST وليس شيئاً آخر
if old_func in content:
    print("✅ دالة games_menu صحيحة")
else:
    # إصلاحها
    new_func = """@app.route('/games')
def games_menu():
    if 'user_type' not in session or session['user_type'] != 'child':
        return redirect(url_for('child_login'))
    return render_template('games_menu.html', games=GAMES_LIST, icons=ICONS, child_name=session['child_name'])"""
    content = content.replace(old_func, new_func)

with open("app.py", "w") as f:
    f.write(content)

print(f"✅ تم تحديث app.py بعدد {len(GAMES_LIST)} لعبة")
