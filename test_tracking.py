import os
import re

print("\n" + "="*60)
print("🔍 TESTING ALL GAMES FOR TRACKER")
print("="*60)

templates_dir = "templates"
games = [f for f in os.listdir(templates_dir) if f.endswith('.html') and f not in ['games_list.html', 'progress.html', 'index.html']]

tracker_count = 0
for game in games:
    with open(f"{templates_dir}/{game}", 'r') as f:
        content = f.read()
        if 'game-tracker.js' in content:
            tracker_count += 1
            print(f"✅ {game}: Tracker present")
        else:
            print(f"❌ {game}: NO TRACKER")

print(f"\n📊 Total: {tracker_count}/{len(games)} games have tracker")
print("="*60)
