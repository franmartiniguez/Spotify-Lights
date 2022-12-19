import urllib.request
from PIL import Image
import requests
from refresh import Refresh
import math
import RPi.GPIO as GPIO
import time

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
SPOTIFY_ACCESS_TOKEN = ''

#function to get the album art of the currently playing song
def get_current_track(access_token):
    #gets the information of the current track playing in a json file
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    #checks to see if there actually is info in the json, if it does, it converts the info into a dictionary 
    #(in cases where a local file song is playing and therefore Spotify has no info about the track)
    try:
        resp_json = response.json()
    except:
        resp_json = ''

    #Gets the album art if there is a track playing with album art, else differentiates it into two categories
    try:
        current_track_art = resp_json['item']['album']['images'][2]['url']
    except:
        if resp_json:
            current_track_art = 'Unrecoverable Art'
        else:
            current_track_art = 'No Track Playing'
    
    return current_track_art

#function to get an average of the rgb values of the album
def get_color(current_track_art):
    #Spotify image names are stored within the url Spotify gives, after /image/
    #so this just finds it using the index where that part ends
    image_name = current_track_art[current_track_art.find('e/') + 2:]

    #gets the image using the specified url and image name and then converts the image into a list of rgb values of its pixels
    urllib.request.urlretrieve(current_track_art, image_name)
    img = Image.open(image_name)
    img = img.convert('RGB')
    
    red = []
    green = []
    blue = []

    #separates each rgb value by color
    for i in img.getdata():
        red.append(i[0])
        green.append(i[1])
        blue.append(i[2])

    mean_red = sum(red)/len(red)
    mean_green = sum(green)/len(green)
    mean_blue = sum(blue)/len(blue)
    mode_red = max(set(red), key=red.count)
    mode_green = max(set(green), key=green.count)
    mode_blue = max(set(blue), key=blue.count)

    average_red = (mean_red + mode_red)/2
    average_green = (mean_green + mode_green)/2
    average_blue = (mean_blue +mode_blue)/2
    
    return [average_red, average_green, average_blue]

def color_distance(current_track_art):
    if current_track_art == 'Unrecoverable Art':
        red, green, blue = [255], [255], [255]
    elif current_track_art == 'No Track Playing':
        red, green, blue = [0], [0], [0]
    else:
        #Spotify image names are stored within the url Spotify gives, after /image/
        #so this just finds it using the index where that part ends
        image_name = current_track_art[current_track_art.find('e/') + 2:]

        #gets the image using the specified url and image name and then converts the image into a list of rgb values of its pixels
        urllib.request.urlretrieve(current_track_art, image_name)
        img = Image.open(image_name)
        img = img.convert('RGB')
        
        red = []
        green = []
        blue = []

        #separates each rgb value by color
        for i in img.getdata():
            red.append(i[0])
            green.append(i[1])
            blue.append(i[2])
        
    average_red = sum(red)/len(red)
    average_green = sum(green)/len(green)
    average_blue = sum(blue)/len(blue)

    distance_to_white = three_dimensional_distance(255, 255, 255, average_red, average_green, average_blue)

    return distance_to_white

#gets the distance between two points in three dimensions
def three_dimensional_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)



def main():
    # #generates a new token to access user's information
    # refresh_token = Refresh()
    # SPOTIFY_ACCESS_TOKEN = refresh_token.refresh()
    # current_track_art = get_current_track(SPOTIFY_ACCESS_TOKEN)

    # # #sets color 
    # # if current_track_art == 'Unrecoverable Art':
    # #     color_values = [255, 255, 255]
    # # elif current_track_art == 'No Track Playing':
    # #     color_values = [0, 0, 0]
    # # else:
    # #     color_values = get_color(current_track_art)
    
    # # print(color_values)
    
    # led_button = 0
    # if color_distance(current_track_art) < 250:
    #     led_button = 1
    

    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # GPIO.setup(14,GPIO.OUT)
    
    # while True:
    #     refresh_token = Refresh()
    #     SPOTIFY_ACCESS_TOKEN = refresh_token.refresh()
    #     current_track_art = get_current_track(SPOTIFY_ACCESS_TOKEN)

    #     if color_distance(current_track_art) < 250:
    #         GPIO.output(14,GPIO.HIGH)
    #     else:
    #         GPIO.output(14,GPIO.LOW)

    #set red,green and blue pins
    redPin = 12
    greenPin = 19
    bluePin = 13
    #set pins as outputs
    GPIO.setup(redPin,GPIO.OUT)
    GPIO.setup(greenPin,GPIO.OUT)
    GPIO.setup(bluePin,GPIO.OUT)

    def turnOff():
        GPIO.output(redPin,GPIO.HIGH)
        GPIO.output(greenPin,GPIO.HIGH)
        GPIO.output(bluePin,GPIO.HIGH)

    def red():
        GPIO.output(redPin,GPIO.LOW)
        GPIO.output(greenPin,GPIO.HIGH)
        GPIO.output(bluePin,GPIO.HIGH)

    def green():
        GPIO.output(redPin,GPIO.HIGH)
        GPIO.output(greenPin,GPIO.LOW)
        GPIO.output(bluePin,GPIO.HIGH)
        
    def blue():
        GPIO.output(redPin,GPIO.HIGH)
        GPIO.output(greenPin,GPIO.HIGH)
        GPIO.output(bluePin,GPIO.LOW)
    
    def white():
        GPIO.output(redPin,GPIO.LOW)
        GPIO.output(greenPin,GPIO.LOW)
        GPIO.output(bluePin,GPIO.LOW)
    
    red()
    time.sleep(1)
    green()
    time.sleep(1)
    blue()
    time.sleep(1)
    white()
    time.sleep(1)
    turnOff()
    
        
if __name__ == "__main__":
    main()