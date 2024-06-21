from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route('/')
def Home():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
