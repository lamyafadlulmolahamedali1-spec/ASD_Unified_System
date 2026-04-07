import re

with open("final_complete_system.py", "r") as f:
    content = f.read()

# تغيير route الرئيسي
old_home_pattern = r"@app\.route\('/'\)\s*def home\(\):.*?return render_template_string\(.*?'''\n.*?'''\s*\)"
new_home = """@app.route('/')
def home():
    return render_template('unified_dashboard.html')"""

content = re.sub(old_home_pattern, new_home, content, flags=re.DOTALL)

with open("final_complete_system.py", "w") as f:
    f.write(content)

print("✅ تم تحديث الصفحة الرئيسية للصفحة الموحدة")
