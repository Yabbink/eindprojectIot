from flask import Flask, request, jsonify, render_template
import tm1637
import time
import threading

# Flask-app initialiseren
app = Flask(__name__)

# TM1637 display instellen op pinnen GPIO13 (CLK) en GPIO19 (DIO)
display = tm1637.TM1637(13, 19, brightness=7)

# Display initialiseren
display.Clear()
display.SetBrightness(1)

# Timerstatus bijhouden (Global variable)
finished = False

# Functie om minuten en seconden op het display te tonen
def display_time(minutes, seconds):
    # Zorg ervoor dat minuten en seconden altijd twee cijfers hebben (bv. 05:09)
    time_digits = [minutes // 10, minutes % 10, seconds // 10, seconds % 10]
    display.Show(time_digits)

# Functie om de timer af te laten tellen
def countdown(minutes, seconds):
    global finished
    finished = False  # Reset de status van de timer

    while minutes >= 0:
        while seconds >= 0:
            display_time(minutes, seconds)
            time.sleep(1)  # Wacht 1 seconde
            seconds -= 1   # Verminder seconden met 1
        minutes -= 1      # Verminder minuten met 1 als seconden 0 bereiken
        seconds = 59      # Reset seconden naar 59 voor de nieuwe minuut

    finished = True  # Zet de status op 'klaar'
    display.Clear()  # Wis het display als de tijd voorbij is

# Webpagina met formulier om de timer in te stellen
@app.route('/')
def index():
    return render_template('index.html')

# API route om de timer te starten
@app.route('/start_timer', methods=['POST'])
def start_timer():
    data = request.json
    minutes = data.get('minutes', 0)
    seconds = data.get('seconds', 0)
    
    # Start de timer in een aparte thread, zodat de webserver blijft draaien
    timer_thread = threading.Thread(target=countdown, args=(minutes, seconds))
    timer_thread.start()
    
    return jsonify({'status': 'Timer gestart', 'minutes': minutes, 'seconds': seconds})

@app.route('/check_timer', methods=['GET'])
def check_timer():
    global finished

    return jsonify({'status': 'done' if finished else 'running'})

# Start de Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



