# pip install these
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from global_hotkeys import *
from threading import Thread
import hashlib
import json
import msvcrt
import os
import pygame
import sys
import websocket # websocket-client

class TTSWebsocketClient():
    def __init__(self):
        self.received_messages = []
        self.closes = []
        self.opens = []
        self.errors = []

        # uncomment for verbose logging
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(f"ws://localhost:16970/xivv",
                                  on_open=self.on_open,
                                  on_message=self.on_message,
                                  on_error=self.on_error,
                                  on_close=self.on_close)
        self.thread = Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

    def on_message(self, ws, message):
        self.received_messages.append(message)
        # uncomment to log the message
        # print(f"Websocket: on_message: {message}")
        jsonData = json.loads(message)
        dialog = jsonData["Payload"]
        # speaker = jsonData["Speaker"]  # not used but could be useful to control AWS voice name
        if dialog:
            dialog = dialog.strip()
            print(f"{dialog}")
            play_dialog(dialog)

    def on_error(self, ws, error):
        self.errors.append(error)
        print(f"TTSWebsocketClient: on_error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.closes.append((close_status_code, close_msg))
        print(f"TTSWebsocketClient: on_close: {close_status_code} - {close_msg}")

    def on_open(self, ws):
        self.opens.append(ws)
        print("TTSWebsocketClient: on_open")

def get_aws_mp3(text, filename):
    try:
        # Request speech synthesis
        global polly
        speechRate = 125 # 100 is default, 125 is faster.  change as desired
        voice = "Joanna" # change as desired
        ssmlText = f"<speak><prosody rate=\"{speechRate}%\">{text}</prosody></speak>"        
        response = polly.synthesize_speech(Text=ssmlText, OutputFormat="mp3",
                                            VoiceId=voice, TextType="ssml")
    except (BotoCoreError, ClientError) as error:        
        print(error) # The service returned an error, exit gracefully
        sys.exit(-1)

    if "AudioStream" in response:
        # cache the audio stream to a file
        with closing(response["AudioStream"]) as stream:
            output = filename
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)


def try_makedir(name):
    try:
        os.mkdir(name)
    except:
        pass

def stop_playing_current_dialog():
    global stopPlayingCurrentDialog
    stopPlayingCurrentDialog = True

def play_dialog(dialog):
    # stop playing dialog if one is playing
    global isDialogPlaying
    if isDialogPlaying:
        global stopPlayingCurrentDialog
        stopPlayingCurrentDialog = True
        while isDialogPlaying:
            pygame.time.wait(10)

    # check cache for the tts dialog
    result = hashlib.sha256(dialog.encode())
    fileName = "cache\\" + result.hexdigest() + ".mp3"
    if not os.path.isfile(fileName):
        get_aws_mp3(dialog, fileName)

    global dialogFileToPlay
    dialogFileToPlay = fileName
    global readyToPlayDialog
    readyToPlayDialog = True

def run():
    global readyToPlayDialog
    global stopPlayingCurrentDialog
    global isDialogPlaying
    global dialogFileToPlay
    isDialogPlaying = False
    stopPlayingCurrentDialog = False
    readyToPlayDialog = False
    dialogFileToPlay = ""

    try_makedir("cache") # create the cache directory if it doesn't exist that stores the tts dialogs

    # press F2 to stop the current dialog playing even if the game is in focus
    bindings = [
        ["f2", None, stop_playing_current_dialog, True],
    ]
    register_hotkeys(bindings)
    start_checking_hotkeys()

    # setup AWS Polly using ENV vars or config file according to AWS docs
    # batch file should look like this:
    #       set AWS_ACCESS_KEY_ID=<YOUR ACCESS KEY>
    #       set AWS_SECRET_ACCESS_KEY=<YOUR SECRET KEY>
    # run this batch file before running this script

    session = Session(region_name="us-west-1") # change to your region as desired
    global polly
    polly = session.client("polly")
    pygame.init()
    pygame.mixer.init()
    client = TTSWebsocketClient()

    keepRunning = True
    while keepRunning:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'q': # press 'q' to quit
                keepRunning = False

        if readyToPlayDialog:
            tada = pygame.mixer.Sound(dialogFileToPlay)
            isDialogPlaying = True
            channel = tada.play()
            while channel.get_busy():
                if stopPlayingCurrentDialog or not keepRunning:
                    channel.stop()
                else:
                    pygame.time.wait(50)
            stopPlayingCurrentDialog = False
            isDialogPlaying = False
            readyToPlayDialog = False
        else:
            pygame.time.wait(50)

    client.ws.close()

run()