import requests

class PepperChat:
    def __init__(self, child_name='lam'):
        self.child_name = child_name
        self.api_url = 'http://localhost:5001'
        
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
        print("\n" + "="*50)
        print("🤖 PEPPER ROBOT - Terminal Chat")
        print("="*50)
        print("Commands: hello | play | help | calm | state | game | exit")
        print("="*50)
        while True:
            try:
                cmd = input("\n💬 You: ").strip().lower()
                if cmd == 'exit':
                    print("🤖 Pepper: Goodbye!")
                    break
                elif cmd == 'hello':
                    print("🤖 Pepper: Hello! How are you today?")
                    self.send_action('positive_reinforcement')
                elif cmd == 'play':
                    print("🤖 Pepper: Let's play a fun game!")
                    self.send_action('start_activity')
                elif cmd == 'help':
                    print("🤖 Pepper: You can do it! Try again.")
                    self.send_action('instruction')
                elif cmd == 'calm':
                    print("🤖 Pepper: Let's take a deep breath.")
                    self.send_action('calming')
                elif cmd == 'state':
                    s = self.get_child_state()
                    print(f"📊 Emotion: {s.get('emotion','neutral')} | Attention: {int(s.get('attention',0.5)*100)}%")
                elif cmd == 'game':
                    print("🎮 Games: emotion_match, color_sort, counting, memory_game")
                else:
                    print(f"🤖 Pepper: I hear you! '{cmd}'")
                    self.send_action('positive_reinforcement')
            except KeyboardInterrupt:
                print("\n👋 Pepper: Goodbye!")
                break

if __name__ == '__main__':
    PepperChat().run()
