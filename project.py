from flask import Flask, jsonify, send_from_directory

import RPi.GPIO as GPIO

import time



# Setup Flask app

app = Flask(__name__, static_folder='static')



# Bin and sensor configuration

BIN_HEIGHT = 10.0  # Bin height in inches



BioTrig = 23

BioEcho = 24

EwasteTrig = 27

EwasteEcho = 22

NonbioTrig = 5

NonbioEcho = 6



GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)



GPIO.setup(BioTrig, GPIO.OUT)

GPIO.setup(BioEcho, GPIO.IN)

GPIO.setup(EwasteTrig, GPIO.OUT)

GPIO.setup(EwasteEcho, GPIO.IN)

GPIO.setup(NonbioTrig, GPIO.OUT)

GPIO.setup(NonbioEcho, GPIO.IN)





def measure_distance(trig_pin, echo_pin):

    GPIO.output(trig_pin, True)

    time.sleep(0.00001)

    GPIO.output(trig_pin, False)



    start_time = time.time()

    stop_time = time.time()



    while GPIO.input(echo_pin) == 0:

        start_time = time.time()



    while GPIO.input(echo_pin) == 1:

        stop_time = time.time()



    time_elapsed = stop_time - start_time

    distance = (time_elapsed * 34300) / 2  # Distance in cm

    distance_in_inches = distance / 2.54   # Convert to inches

    return distance_in_inches





def calculate_fill_level(distance):

    if distance >= BIN_HEIGHT:

        return 0  # Bin is empty

    elif distance <= 0:

        return 100  # Bin is full

    else:

        fill_level = ((BIN_HEIGHT - distance) / BIN_HEIGHT) * 100

        return round(fill_level)









@app.route('/get_bin_levels', methods=['GET'])

def get_bin_levels():

    # Measure distance for each bin and calculate fill levels

    bin_levels = []

    distance1 = measure_distance(BioTrig, BioEcho)

    distance2 = measure_distance(EwasteTrig, EwasteEcho)

    distance3 = measure_distance(NonbioTrig, NonbioEcho)



    fill_level1 = calculate_fill_level(distance1)

    fill_level2 = calculate_fill_level(distance2)

    fill_level3 = calculate_fill_level(distance3)



    bin_levels=[fill_level1, fill_level2, fill_level3]





    # Return the data with the correct keys

    return jsonify(bin_levels)





@app.route('/')

def serve_index():

    return send_from_directory('static', 'index.html')



if __name__ == '__main__':

    try:

        app.run(host='0.0.0.0', port=5000)

    except KeyboardInterrupt:

        pass

    finally:

        GPIO.cleanup()

