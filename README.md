# xivvToPolly

This is a websocket client for use with with xiv voices.  It downloads the TTS data from AWS polly, caches it, and plays it. 

## Setup
- Set up AWS Polly according to the TextToTalk docs: https://github.com/karashiiro/TextToTalk/wiki/Creating-access-keys-for-Amazon-Polly
- Create the folder `%USERPROFILE%\.aws`
- Open Notepad. In it, put this, substituting your access key and secret key from Polly:
```
    [default]
    aws_access_key_id = YOUR ACCESS KEY
    aws_secret_access_key = YOUR SECRET KEY
```
- Save this file as `"%USERPROFILE%\.aws\credentials"`. The quotation marks around the filename are important. If you get a text document, turn on file extensions and remove .txt
- Run `pip install -r requirements.txt` to install dependencies.
- Go to XIV Voices, click the grey button next to the microphone button, and start the websocket on port 16970.
- Run `python3 xivvToPolly.py`. You should see:
```
    pygame 2.5.2 (SDL 2.28.3, Python 3.12.1)
    Hello from the pygame community. https://www.pygame.org/contribute.html
    TTSWebsocketClient: on_open
```

## Troubleshooting
- If you see:
  - `TTSWebsocketClient: on_error: [WinError 10061] No connection could be made because the target machine actively refused it`
    - Start the second websocket in XIV Voices: click the grey button next to the microphone button, and start the websocket on port 16970.
  - `Unable to locate credentials`
    - Make sure that the file `%USERPROFILE%\.aws\credentials` exists: open notepad, press ctrl-O, copy and paste that path into the filename box, click open.

## Tweaks
- Change speechRate and voice variables in python script as desired.
- Change region_name variables in python script as desired.
- Change F2 to another hotkey in python script as desired.

## Usage
- Press 'q' to quit
- Press 'F2' to stop playing the currently playing dialog.  This is a global hotkey and will work even when FF is active.

