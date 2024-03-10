from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import webbrowser

app = Flask(__name__)
auth = HTTPBasicAuth()

# you can change the login username and password here
users = {
    "admin": "admin"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

recent_links = []

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html', recent_links=recent_links)

@app.route('/open_link', methods=['POST'])
@auth.login_required
def open_link():
    link = request.form['link']
    if link:
        webbrowser.open(link, new=2)
        recent_links.append(link)
    return redirect(url_for('index'))

@app.route('/close_link/<int:index>')
@auth.login_required
def close_link(index):
    if 0 <= index < len(recent_links):
        closed_link = recent_links.pop(index)
        return f'Closed: {closed_link}'
    return 'Invalid index'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
