from flask import Flask, render_template
from threading import Thread

app = Flask('')

@app.route('/')
def index():
  return render_template('index.html', bot = bot_obj)
def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive(bot):
  global bot_obj
  bot_obj = bot
  server = Thread(target=run)
  server.start()