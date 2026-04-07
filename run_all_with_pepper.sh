#!/bin/bash
echo "========================================="
echo "🤖 ASD Complete System + Pepper in PyBullet"
echo "========================================="

# نافذة 1: Dashboard
gnome-terminal --window --title="📊 DASHBOARD" -- bash -c "
cd ~/Desktop/ASD_Final_Working
echo '📊 Starting Dashboard on http://localhost:5001'
python3 app.py
exec bash" &

sleep 3

# نافذة 2: Emotion Detection
gnome-terminal --window --title="📷 EMOTION DETECTION" -- bash -c "
cd ~/Desktop/ASD_Final_Working
echo '📷 Starting Emotion Detection...'
python3 detection.py
exec bash" &

sleep 2

# نافذة 3: Pepper Chat
gnome-terminal --window --title="🤖 PEPPER CHAT" -- bash -c "
cd ~/Desktop/ASD_Final_Working
echo '🤖 Starting Pepper Chat...'
python3 pepper_chat.py
exec bash" &

sleep 2

# نافذة 4: Pepper in PyBullet (يطارد البالونات)
gnome-terminal --window --title="🎈 PEPPER IN PYBULLET" -- bash -c "
cd ~/Desktop/ASD_Final_Working
echo '🎈 Starting Pepper chasing balloons...'
python3 pepper_pybullet_balloon.py
exec bash" &

echo ""
echo "========================================="
echo "✅ ALL SYSTEMS RUNNING"
echo "========================================="
echo "📊 Dashboard: http://localhost:5001"
echo "🤖 Pepper Chat: Type commands in terminal"
echo "🎈 Pepper in PyBullet: Robot chasing balloons"
echo "📷 Emotion Detection: Camera with YOLO"
echo "========================================="
echo ""
echo "💬 In Pepper Chat terminal, type:"
echo "   hello, play, help, calm, state, game, exit"
echo ""
echo "📌 To stop: Close all windows or Ctrl+C in each"
echo "========================================="

wait
