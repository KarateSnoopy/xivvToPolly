# xivvToPolly

This is a websocket client for use with with xiv voices.  It downloads the TTS data from AWS polly, caches it, and plays it. 

## Setup
- Setup AWS Polly using ENV vars or config file according to AWS docs
- Batch file should look like this:

    set AWS_ACCESS_KEY_ID=YOUR ACCESS KEY

    set AWS_SECRET_ACCESS_KEY=YOUR SECRET KEY

- See set-aws.cmd for an example.  You'll need to edit it with your secret values from AWS portal.
- Run this batch file before running this python script.
- Use "pip install" until you don't get dependency errors.  See top of python for required import modules.
- Go to XIV Voices, click button and start the websocket on port 16970.  When running the python script, it should automatically connect.  You can stop and start the python script as desired without needing to mess with XIV Voices.

## Tweaks
- Change speechRate and voice variables in python script as desired.
- Change region_name variables in python script as desired.
- Change F2 to another hotkey in python script as desired.

## Usage
- Press 'q' to quit
- Press 'F2' to stop playing the currently playing dialog.  This is a global hotkey and will work even when FF is active.

