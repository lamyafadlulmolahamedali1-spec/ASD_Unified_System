from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "<h1>Extra Dashboard</h1><p>Additional analytics and monitoring tools</p>"
if __name__ == '__main__': app.run(host='0.0.0.0', port=5007, debug=True)
