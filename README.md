# Spotify RFID Controller

This project is a MicroPython program designed for the Raspberry Pi Pico W microcontroller. It enables you to control Spotify playback by scanning RFID cards using an RC522 RFID reader. When an RFID card is detected, the program communicates with the Spotify API to perform actions such as playing a specific track or toggling playback (pause/play), based on the unique ID of the scanned card.

![Project Diagram](images/pico.png)

## Requirements

* Spotify Premium account (required for API access)

### Hardware
* Raspberry Pi Pico W microcontroller
* RFID RC522 transceiver
* RFID cards or tags

### Software
* MicroPython (flashed onto the Raspberry Pi Pico W)
* mfrc522 library

## Basic Setup

1.  **Wire RC522 to Pico W:** Connect the RFID reader to your Raspberry Pi Pico W.
2.  **Configure Credentials:**
    * Set your Wi-Fi `ssid` and `password` in `main.py`.
    * Run `code_tokens.py` (after updating its `CLIENT_ID` and `CLIENT_SECRET`) to obtain the initial `code`, `token`, and `refresh_token`. Update these in `main.py`.
3.  **Map RFID Cards:** In `main.py`, edit the `card_dictionary` to link your RFID card IDs to Spotify track IDs or actions.
