from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from scanner import Scanner


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/standby')
def standby():
    s = Scanner()
    s.standby()
    return jsonify(None)

@app.route('/safe')
def safe():
    s = Scanner()
    s.scan()
    r = s.safe()
    return jsonify(r)

@app.route('/sentry')
def sentry():
    s = Scanner()
    s.scan()
    r = s.sentry()
    return jsonify(r)


if __name__ == '__main__':
    app.run(debug=True)