import re

with open("final_complete_system.py", "r") as f:
    content = f.read()

# إضافة iframe لعرض الألعاب داخل الصفحة
iframe_section = '''
<div style="margin: 20px 0;">
    <button onclick="toggleGames()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 10px; cursor: pointer;">
        🎮 Show/Hide Games Portal
    </button>
    <div id="gamesFrame" style="display: none; margin-top: 20px;">
        <iframe src="http://localhost:5009" width="100%" height="600" style="border: none; border-radius: 20px;"></iframe>
    </div>
</div>
<script>
function toggleGames() {
    var frame = document.getElementById('gamesFrame');
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
    } else {
        frame.style.display = 'none';
    }
}
</script>
'''

# إضافة قبل نهاية body
content = content.replace('</body>', iframe_section + '\n</body>')

with open("final_complete_system.py", "w") as f:
    f.write(content)

print("✅ تم إضافة iframe لعرض الألعاب داخل الصفحة")
