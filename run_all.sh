#!/bin/bash
echo "========================================="
echo "🤖 ASD COMPLETE SYSTEM"
echo "========================================="

# تشغيل النظام الرئيسي (5001)
gnome-terminal --tab --title="MAIN DASHBOARD (5001)" -- bash -c "cd ~/Desktop/ASD_Unified_System && python3 final_complete_system.py; exec bash"

sleep 3

# تشغيل Games Portal (5009)
gnome-terminal --tab --title="GAMES PORTAL (5009)" -- bash -c "cd ~/Desktop/ASD_Unified_System && python3 app_games.py; exec bash"

sleep 2

# تشغيل Pepper Chat
gnome-terminal --tab --title="PEPPER CHAT" -- bash -c "cd ~/Desktop/ASD_Unified_System && python3 pepper_chat.py; exec bash"

echo ""
echo "========================================="
echo "✅ ALL SYSTEMS RUNNING!"
echo "========================================="
echo "📍 Main Dashboard: http://localhost:5001"
echo "📍 Games Portal: http://localhost:5009"
echo "📍 AI Chat: http://localhost:5009/game/ai_chat"
echo "📍 Pepper Chat: Terminal window"
echo "========================================="
