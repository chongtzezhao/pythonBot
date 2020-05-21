from flask import Flask, render_template_string
from threading import Thread
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
  return render_template_string('<script>window.location="https://www.youtube.com/watch?v=dQw4w9WgXcQ"</script>')

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t1 = Thread(target=run)
  t1.start()