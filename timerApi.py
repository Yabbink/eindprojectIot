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

# Timerstatus bijhouden (Global variables)
finished = False
timer_stopped = False
stopped_by_user = False  # Variabele om bij te houden of de gebruiker de timer gestopt heeft

# Functie om uren, minuten en seconden op het display te tonen
def display_time(hours, minutes, seconds):
    if hours > 0:
        # Als er uren over zijn, toon uren en minuten
        time_digits = [hours // 10, hours % 10, minutes // 10, minutes % 10]
    else:
        # Als er geen uren meer zijn, toon alleen minuten en seconden
        time_digits = [minutes // 10, minutes % 10, seconds // 10, seconds % 10]

    display.Show(time_digits)

# Functie om de timer af te laten tellen
def countdown(hours, minutes, seconds):
    global finished, timer_stopped, stopped_by_user
    finished = False  # Reset de status van de timer
    timer_stopped = False  # Reset de stopflag
    stopped_by_user = False  # Reset de 'stopped by user'-flag

    while hours >= 0:
        if timer_stopped:  # Check of er een stopverzoek is
            display.Clear()
            stopped_by_user = True  # Markeer dat de timer handmatig is gestopt
            return  # Stop de timer en verlaat de functie
        while minutes >= 0:
            if timer_stopped:  # Check binnen de minuten-lus
                display.Clear()
                stopped_by_user = True  # Markeer dat de timer handmatig is gestopt
                return  # Stop de timer en verlaat de functie
            while seconds >= 0:
                if timer_stopped:  # Check binnen de seconden-lus
                    display.Clear()
                    stopped_by_user = True  # Markeer dat de timer handmatig is gestopt
                    return  # Stop de timer en verlaat de functie
                display_time(hours, minutes, seconds)  # Toon de juiste tijd
                time.sleep(1)  # Wacht 1 seconde
                seconds -= 1   # Verminder seconden met 1
            minutes -= 1      # Verminder minuten met 1 als seconden 0 bereiken
            seconds = 59      # Reset seconden naar 59 voor de nieuwe minuut
        if hours > 0:        # Verminder uren alleen als uren > 0
            hours -= 1       # Verminder uren met 1 als minuten 0 bereiken
            minutes = 59     # Reset minuten naar 59 voor het nieuwe uur

    finished = True  # Zet de status op 'klaar'
    display.Clear()  # Wis het display als de tijd voorbij is

# Webpagina met formulier om de timer in te stellen
@app.route('/')
def index():
    return render_template('index.html')

# API route om de timer te starten
@app.route('/start_timer', methods=['POST'])
def start_timer():
    global finished, timer_stopped, stopped_by_user
    
    # Reset alle relevante variabelen
    finished = False
    timer_stopped = False
    stopped_by_user = False
    
    data = request.json
    hours = data.get('hours', 0)
    minutes = data.get('minutes', 0)
    seconds = data.get('seconds', 0)
    
    # Start de timer in een aparte thread, zodat de webserver blijft draaien
    timer_thread = threading.Thread(target=countdown, args=(hours, minutes, seconds))
    timer_thread.start()
    
    return jsonify({'status': 'Timer gestart', 'hours': hours, 'minutes': minutes, 'seconds': seconds})

# API route om de timer te stoppen
@app.route('/stop_timer', methods=['GET'])
def stop_timer():
    global timer_stopped
    timer_stopped = True  # Zet de vlag om de timer te stoppen
    return jsonify({'status': 'Timer gestopt'})

# API om de timerstatus te controleren
@app.route('/check_timer', methods=['GET'])
def check_timer():
    global finished, stopped_by_user

    if stopped_by_user:
        return jsonify({'status': 'stopped'})
    elif finished:
        return jsonify({'status': 'done'})
    else:
        return jsonify({'status': 'running'})

# Start de Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




