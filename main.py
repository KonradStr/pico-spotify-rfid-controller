from mfrc522 import MFRC522
import utime
import ujson
import base64
import requests
import urequests
import network

client_id = "..."
client_secret = "..."
code = "..."
token = "..."
refresh_token = "..."


user_headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Content-Length" : "0"
}

# mapping of RFID card IDs to Spotify track IDs
# card IDs listed are specific to tested RFID cards and may not work with other cards
# to make this work, you will need to replace these IDs with the IDs of your RFID cards
card_dictionary = {
    "4144417555": "toggle_playback", # pause/play
    "3976869773": "2nFaT0t36H6UX3wN3Vxvjm", # California - White2115
    "3974820045": "4gsJGePgdNmdXBnnZOuEMu", # Kocham piwo - Big Cyc
    "906769347" : "4AFlChQQJbB1MOCgOiiyYc", # Drums - James Hype
    "3420368973": "1PVTvvxpSkyJWemW1CwVVk", # Fly Me To The Moon - Frank Sinatra
    "3285003885": "60a0Rd6pjrkxjPbaKzXjfq", # In the End - Linkin Park
    "3408315469": "5ChkMS8OtdzJeqyybCc9R5", # Billie Jean - Michael Jackson
    "3979990173": "6TaPIrwDMIml6iMEqMUHK6", # Nocturne Op. 9 No 2 - Fryderyk Chopin
    "3398019885": "3PQLYVskjUeRmRIfECsL0X", # No Woman, No Cry - Bob Marley
    "3978952669": "4sAPyrIRUVKCax5d1bt96D", # Ściernisko - Golec uOrkiestra
    "3410021821": "4Wm4rtJTkXIGOIWrEvTtzN", # Zacznij od Bacha - Zbigniew Wodecki
    "3402656669": "7MJQ9Nfxzh8LPZ9e9u68Fq", # Lose Yourself - Eminem
    "2374600228": "1OzlBug7c2LKPvIoMkuQhe", # Parostatek - Krzysztof Krawczyk
}

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        utime.sleep(1)
    print("Network connected")


def toggle_playback():
    status = requests.get('https://api.spotify.com/v1/me/player', headers=user_headers)
    if (status.json()['is_playing']) == True: 
        requests.put('https://api.spotify.com/v1/me/player/pause', headers=user_headers)
    else:
        requests.put('https://api.spotify.com/v1/me/player/play', headers=user_headers)
    

def card_ID_handling(card_ID):
    if card_ID in card_dictionary:
        action = card_dictionary[card_ID]
        if action == "toggle_playback":
            toggle_playback()
        else:
            requests.post(f'https://api.spotify.com/v1/me/player/queue?uri=spotify%3Atrack%3A{action}', headers=user_headers)
            requests.post('https://api.spotify.com/v1/me/player/next', headers=user_headers)
        
        
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
 
ssid = '...'
password = '...'
connect_to_wifi(ssid, password)

print("Bring TAG closer...\n")

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))
            card_ID_handling(str(card))
            
    utime.sleep_ms(500) 
