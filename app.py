from flask import Flask, render_template, request, redirect, url_for, session
import random
import requests


app = Flask(__name__)
API_KEY="4eebed6336231b09aa4087c5391e953a"
app.secret_key = "secret"

# Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Calculator
@app.route('/calculator', methods=["GET", "POST"])
def calculator():
    result = ""
    expression = ""
    if request.method == "POST":
        expression = request.form.get("expression", "")
        try:
            result = eval(expression)
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("calculator.html", result=result, expression=expression)

# Currency Converter
@app.route('/converter', methods=['GET', 'POST'])
def converter():
    converted = None
    if request.method == 'POST':
        amount = request.form.get('amount')  # Safe access
        if amount:
            try:
                amount = float(amount)
                # Sample conversion logic (INR to USD)
                converted = round(amount / 83.0, 2)
            except ValueError:
                converted = "Invalid amount entered!"
    return render_template('converter.html', converted=converted)
# Rock Paper Scissors

@app.route('/rps', methods=['GET', 'POST'])
def rps():
    result = ""
    if request.method == 'POST':
        user = request.form['choice']
        comp = random.choice(['rock', 'paper', 'scissors'])
        if user == comp:
            result = "Draw!"
        elif (user == "rock" and comp == "scissors") or \
             (user == "scissors" and comp == "paper") or \
             (user == "paper" and comp == "rock"):
            result = "You Win!"
        else:
            result = "Computer Wins!"
    return render_template('rps.html', result=result)

# Guessing Game
@app.route('/guess', methods=['GET', 'POST'])
def guess():
    msg = ""
    if 'number' not in session:
        session['number'] = random.randint(1, 10)
    if request.method == 'POST':
        guess = int(request.form['guess'])
        if guess == session['number']:
            msg = "Correct!"
            session.pop('number', None)
        elif guess < session['number']:
            msg = "Too Low!"
        else:
            msg = "Too High!"
    return render_template('guess.html', message=msg)

# Register/Login
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        users[uname] = pwd
        msg = "Registered successfully!"
    return render_template('register.html', message=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if users.get(uname) == pwd:
            msg = "Login successful"
        else:
            msg = "Login failed"
    return render_template('login.html', message=msg)

@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather_data = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # <-- Replace with your API key
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()
                if data.get("cod") == 200:
                    weather_data = {
                        "city": data["name"],
                        "temp": data["main"]["temp"],
                        "desc": data["weather"][0]["description"].title(),
                        "icon": data["weather"][0]["icon"],
                    }
                else:
                    error = data.get("message", "City not found")
            except Exception as e:
                error = "Error fetching weather"
        else:
            error = "Please enter a city name"
    return render_template("weather.html", weather=weather_data, error=error)


if __name__ == '__main__':
    app.run(debug=True)