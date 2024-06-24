from flask import Flask, render_template, redirect, session, request

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'id1': 'password123',
    'id2': 'password456'
}

@app.route('/')
def Home():
    return render_template('login2.html')
    # return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
