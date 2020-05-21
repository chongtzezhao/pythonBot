from flask import Flask, render_template_string
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
  return render_template_string('''<!DOCTYPE html>
<html>
    <head><script>window.location="https://www.youtube.com/watch?v=dQw4w9WgXcQ"</script></head>
</html>''')

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t1 = Thread(target=run)
  t1.start()