from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Set a secret key for sessions

# Database initialization
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
conn.commit()
conn.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('SELECT password FROM users WHERE username=?', (username,))
        result = c.fetchone()

        conn.close()

        if result and result[0] == password:
            # Authentication successful
            # You can redirect the user to a different page or set a session variable
            return redirect(url_for('event'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('index.html', error=error)

    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

        conn.close()

        # Registration successful
        # You can redirect the user to a different page or set a session variable
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        selected_event = request.form['event']

        # Process the selected event here
        # You can redirect the user to a dashboard or perform any other action based on the selected event

        return render_template('dashboard.html', event=selected_event)

    return render_template('event.html')


@app.route('/dashboard')
def dashboard():
    # Retrieve the selected event from the session or any other mechanism
    selected_event = request.args.get('event')

    return render_template('dashboard.html', event=selected_event)


if __name__ == '__main__':
    app.run(debug=True)
