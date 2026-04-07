import requests
import subprocess
import os

class PepperChat:
    def __init__(self, child_name='lam'):
        self.child_name = child_name
        self.api_url = 'http://localhost:5001'
        self.game_process = None
        
    def open_balloon_game(self):
        """Open pepper balloon game in new terminal"""
        try:
            subprocess.Popen(['gnome-terminal', '--tab', '--title=BALLOON GAME', 
                             '--', 'bash', '-c', 
                             'cd ~/Desktop/ASD_Final_Working && python3 pepper_balloon_game.py; exec bash'])
            return "🎈 Opening balloon game! Pepper will chase and catch balloons! Have fun!"
        except:
            return "⚠️ Could not open game. Make sure pepper_balloon_game.py exists."
    
    def open_asd_games(self):
        """Open ASD games folder"""
        games_path = os.path.expanduser("~/Desktop/ASD_Final_Working")
        try:
            subprocess.Popen(['nautilus', games_path])
            return "🎮 Opening your ASD games folder! Choose a game to play!"
        except:
            return "🎮 Games folder not found!"
    
    def send_action(self, action):
        try:
            requests.post(f'{self.api_url}/api/therapy-action', 
                         json={'child': self.child_name, 'action': action}, timeout=1)
            print(f"🤖 Pepper: {action}")
        except:
            print("⚠️ Dashboard not connected")
    
    def get_child_state(self):
        try:
            r = requests.get(f'{self.api_url}/api/child-state/{self.child_name}', timeout=1)
            return r.json()
        except:
            return {'emotion': 'neutral', 'attention': 0.5}
    
    def run(self):
        print("\n" + "="*55)
        print("🤖 PEPPER ROBOT - ASD Complete System")
        print("="*55)
        print("Commands:")
        print("   hello  - Greet Pepper")
        print("   play   - Play the balloon game!")
        print("   games  - Open ASD games folder")
        print("   state  - See child's emotion")
        print("   calm   - Calming activity")
        print("   help   - Get encouragement")
        print("   exit   - Quit")
        print("="*55)
        print("\n🤖 Pepper: Hello! I'm Pepper! I love catching balloons! Type 'play' to start! 🎈")
        
        while True:
            try:
                cmd = input("\n💬 You: ").strip().lower()
                if cmd == 'exit':
                    print("🤖 Pepper: Goodbye! See you soon!")
                    break
                elif cmd == 'hello':
                    print("🤖 Pepper: Hello! How are you today? 😊")
                    self.send_action('positive_reinforcement')
                elif cmd == 'play':
                    result = self.open_balloon_game()
                    print(f"🤖 Pepper: {result}")
                    self.send_action('start_game')
                elif cmd == 'games':
                    result = self.open_asd_games()
                    print(f"🤖 Pepper: {result}")
                elif cmd == 'state':
                    s = self.get_child_state()
                    print(f"📊 Emotion: {s.get('emotion','neutral')} | Attention: {int(s.get('attention',0.5)*100)}%")
                elif cmd == 'calm':
                    print("🤖 Pepper: Let's take a deep breath together... In... Out... You're doing great! 🧘")
                    self.send_action('calming')
                elif cmd == 'help':
                    print("🤖 Pepper: You can do it! Try one more time! You're amazing! 🌟")
                    self.send_action('instruction')
                else:
                    print(f"🤖 Pepper: That's interesting! Tell me more about '{cmd}'! 🎈")
                    self.send_action('positive_reinforcement')
            except KeyboardInterrupt:
                print("\n🤖 Pepper: Goodbye!")
                break

if __name__ == '__main__':
    PepperChat().run()
