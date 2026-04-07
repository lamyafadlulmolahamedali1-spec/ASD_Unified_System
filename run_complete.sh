#!/bin/bash
echo "========================================="
echo "🤖 ASD COMPLETE SYSTEM"
echo "========================================="
echo ""

# تشغيل Gazebo مع Pepper (نافذة منفصلة)
echo "🚀 Starting Gazebo with Pepper Robot..."
gnome-terminal --tab --title="🤖 PEPPER GAZEBO" -- bash -c "
source /opt/ros/humble/setup.bash
cd ~/Desktop/ASD_Final_Working
gazebo --verbose worlds/empty.world &
sleep 5
ros2 run gazebo_ros spawn_entity.py -entity pepper -file ~/pepper_ws/urdf/pepper.urdf -x 0 -y 0 -z 0.1
exec bash"

sleep 5

# تشغيل Flask Dashboard (الألعاب)
echo "🎮 Starting Games Portal..."
gnome-terminal --tab --title="🎮 GAMES" -- bash -c "
cd ~/Desktop/ASD_Final_Working
python3 app.py
exec bash"

sleep 3

# تشغيل Detection (الكاميرا)
echo "📷 Starting Emotion/Face/Object Detection..."
gnome-terminal --tab --title="📷 DETECTION" -- bash -c "
cd ~/Desktop/ASD_Final_Working
python3 detection.py
exec bash"

sleep 2

# تشغيل Pepper Chat
echo "💬 Starting Pepper Chat Interface..."
gnome-terminal --tab --title="💬 PEPPER CHAT" -- bash -c "
cd ~/Desktop/ASD_Final_Working
python3 pepper_chat.py
exec bash"

echo ""
echo "========================================="
echo "✅ ALL SYSTEMS RUNNING!"
echo "========================================="
echo "🤖 Pepper Robot: In Gazebo window"
echo "🎮 Games Portal: http://localhost:5001"
echo "📷 Detection: Camera window"
echo "💬 Pepper Chat: Type commands in terminal"
echo "========================================="
echo ""
echo "💬 Commands for Pepper Chat:"
echo "   hello | play | help | calm | state | game | exit"
echo "========================================="

wait
