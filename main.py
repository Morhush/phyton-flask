from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route('/')
def index():
    n = random.randint(0, 1000)
    k = random.randint(1000, 5000)
    return render_template('index.html', n=n)


@app.route('/login')
def login():
    return render_template('index.html')


@app.route('/Denis')
def Denis():
    return "<h2>O ja suda</h2>"

# Лише для локального сервера (закоментувати)
if __name__ == '__main__':
    app.run(debug=True)





