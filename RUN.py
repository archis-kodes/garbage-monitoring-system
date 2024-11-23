from flask import Flask, jsonify, send_from_directory
import RPi.GPIO as GPIO # type: ignore
import time

app = Flask(__name__, static_folder='static')


#SET BIN HEIGHT

BIN_HEIGHT = 11.0  #Inches


#PIN DECLARATION

BioTrig = 17

BioEcho = 27

NonbioTrig = 22

NonbioEcho = 25

RAIN_SENSOR_PIN = 14

servo_pin = 18

TRIG = 23

ECHO = 24


#BCM SETUP

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)



#PIN SETUP

GPIO.setup(BioTrig, GPIO.OUT)

GPIO.setup(BioEcho, GPIO.IN)

GPIO.setup(NonbioTrig, GPIO.OUT)

GPIO.setup(NonbioEcho, GPIO.IN)

GPIO.setup(TRIG, GPIO.OUT)

GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)

GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)

pwm.start(0)

'''****************************************************************************************************
***********************************      USER DEFINED FUNCTIONS     ***********************************
****************************************************************************************************'''


def measure_depth(trig_pin, echo_pin):

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




def measure_distance():

    GPIO.output(TRIG, False)

    time.sleep(0.1)

    GPIO.output(TRIG, True)

    time.sleep(0.00001)

    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:

        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:

        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    return round(distance, 2)

def set_angle(angle):

    duty_cycle = 2 + (angle / 18)

    pwm.ChangeDutyCycle(duty_cycle)

    time.sleep(0.5)

    pwm.ChangeDutyCycle(0)

print("Raindrop sensor monitoring started. Press Ctrl+C to stop.")




def wetwaste():

    set_angle(135)

    time.sleep(3)

    set_angle(90)

    time.sleep(1)




def drywaste():
    set_angle(45)

    time.sleep(3)

    set_angle(90)

    time.sleep(1) 




@app.route('/get_bin_levels', methods=['GET'])

def get_bin_levels():

    bin_levels = []


    distance1 = measure_depth(BioTrig, BioEcho)

    distance2 = measure_depth(NonbioTrig, NonbioEcho)



    fill_level1 = calculate_fill_level(distance1)

    fill_level2 = calculate_fill_level(distance2)



    bin_levels=[fill_level1, fill_level2]

    return jsonify(bin_levels)


@app.route('/')

def serve_index():

    return send_from_directory('static', 'index.html')


'''****************************************************************************************************
***********************************          MAIN FUNCTION          ***********************************
****************************************************************************************************'''


if __name__ == '__main__':

    try:

        while True:

            app.run(host='192.168.137.139', port=5000)

            time.sleep(1.5)

            if (measure_distance()<=30):

                if GPIO.input(RAIN_SENSOR_PIN) == GPIO.LOW:

                    print("Wet Waste!")

                    wetwaste()

                else:

                    print("Dry Waste!")

                    drywaste()

            
            time.sleep(1)
            
    except KeyboardInterrupt:

        print("Exiting program.")

    finally:

        GPIO.cleanup()
