from flask import Flask, render_template, request
from main import get_top_100

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/top-followers/<username>')
def get_top(username):
    followers = get_top_100(username)
    return render_template('followers.html', followers = followers )

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
