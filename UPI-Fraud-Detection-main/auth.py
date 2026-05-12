from flask import Blueprint, render_template, request, redirect, session

auth = Blueprint('auth', __name__)

users = {}   # simple memory users


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users[username] = password
        return redirect('/login')

    return render_template("signup.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.get(username) == password:
            session['user'] = username
            return redirect('/')

        return "Invalid credentials"

    return render_template("login.html")


@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')