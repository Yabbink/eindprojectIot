import tm1637
import time

display = tm1637.TM1637(13, 19, brightness=7)

display.Clear()
display.SetBrightness(1)

# Functie om minuten en seconden op het display te tonen
def display_time(minutes, seconds):
    display.numbers(minutes, seconds)

# Functie om de timer van 5 minuten af te laten tellen
def countdown(minutes, seconds):
    while minutes >= 0:
        while seconds >= 0:
            display_time(minutes, seconds)
            time.sleep(1)  # Wacht 1 seconde
            seconds -= 1   # Verminder seconden met 1
        minutes -= 1      # Verminder minuten met 1 als seconden 0 bereiken
        seconds = 59      # Reset seconden naar 59 voor de nieuwe minuut

# Timer van 5 minuten starten
countdown(5, 0)