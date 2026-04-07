import re

# قراءة الملف
with open("final_complete_system.py", "r") as f:
    content = f.read()

# البحث عن قسم الألعاب في قالب child dashboard وإضافة زر
old_games_section = '<div class="games-grid">'
new_games_section = '''
<div style="text-align: center; margin: 20px 0;">
    <a href="http://localhost:5009" target="_blank" 
       style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
              color: white; padding: 15px 40px; border-radius: 50px; text-decoration: none; 
              font-size: 18px; font-weight: bold; margin: 10px;">
        🎮 Open All 52 Games 🎮
    </a>
    <p style="font-size: 12px; color: #888;">Click to open the full games portal</p>
</div>
<div class="games-grid">'''

# استبدال
content = content.replace(old_games_section, new_games_section)

# حفظ الملف
with open("final_complete_system.py", "w") as f:
    f.write(content)

print("✅ تم إضافة زر الألعاب إلى Child Dashboard")
print("📍 الزر سيفتح: http://localhost:5009")
