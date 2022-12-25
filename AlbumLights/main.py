import urllib.request
from PIL import Image
import requests
from refresh import Refresh
import board
import neopixel
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

def main():
    pixels = neopixel.NeoPixel(board.D18, 60)
    try:
        while True:
            refresh_token = Refresh()
            SPOTIFY_ACCESS_TOKEN = refresh_token.refresh()
            current_track_art = get_current_track(SPOTIFY_ACCESS_TOKEN)

            if current_track_art == 'Unrecoverable Art':
                color_values = [255, 255, 255]
            elif current_track_art == 'No Track Playing':
                color_values = [0, 0, 0]
            else:
                color_values = get_color(current_track_art)
                
            if max(color_values) == color_values[0]:
                pixels.fill((color_values[0], color_values[1]/3, color_values[2]/3))
            elif max(color_values) == color_values[1]:
                pixels.fill((color_values[0]/3, color_values[1], color_values[2]/3))
            else:
                pixels.fill((color_values[0]/3, color_values[1]/3, color_values[2]))


    except:
        pixels.fill((0,0,0))
        
if __name__ == "__main__":
    main()