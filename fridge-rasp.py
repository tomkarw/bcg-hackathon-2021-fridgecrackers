import time
import requests

import RPi.GPIO as GPIO
import dht11

MAX_TEMP = 10

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
dht = dht11.DHT11(pin = 21)

temp_list = [0 for _ in range(10)]

def run():
    while True:
        result = dht.read()
        
        if result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)

            log_data(result.temperature, result.humidity)
               
            temp_list.append(result.temperature)
            temp_list.pop(0)
            print(temp_list)
    
            # if last 10 temp recording are above threshold, make an alert
            if all([temp > MAX_TEMP for temp in temp_list]):
                alert(result)

            time.sleep(3)
        else:
            pass
            # print("Error: %d" % result.error_code)
    
def alert(result):
    print(f"ALERT!: temprerature {result.temperature} is above the threshold of {MAX_TEMP}")

def log_data(temperature, humidity):
    print('Make request')

    url = "https://google.com"
    response = requests.get(url)
    if response is not None and response.status_code < 400:
        print('Request successful')
        print(response.text[:20])
    else:
        print('Request failed')

if __name__ == "__main__":
    run()
