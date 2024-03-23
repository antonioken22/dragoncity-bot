# dragoncity-bot

A Dragon City (Windows Desktop) Bot that automates mundane tasks. Works only with 1920x1080p desktop resolution.

## Demo Video

v1.1: https://youtu.be/OgetBWFXCHU?si=GipKLMLb9a_G-L2L
v1.2: Coming soon...

## Main Features

- Uses `pyautogui`
- Simple System Dialogues With Instructions
- Visual Studio Code Terminal Logging
- Can Be Run Like An Executable By Double Clicking `main.py`
- More to come

## Bot Tasks Available

- Collect Gold and Food (up to 9th Island only)
- Watch Dragon TV Island Ads
- Watch Greenhouse Building Ads
- Watch Hatchery Ads
- League Auto Combat
- Dragon Rescue Auto Combat
- Unli Terra + Terra Breeding (up to 40 Cycles only)
- Unli Terra Hatching (up to 40 Cycles only) <-- Latest Feature
- Arena Fight to Lose Points
- More to come

## How to use

- Clone this repository into your own machine
- Run the code below in your Visual Studio Code Terminal

```shell
pip install -r requirements.txt
```

- Open your Dragon City Desktop Application
- And run `main.py`

## How does it work?

- It searches on the screen a match of a saved `.png` image
- Clicks it or just looks it up and see if it's there
- And cycles through the tasks per set `delay` which is `0.5`s by default

## Image not found even if it's there

- Try recreating the screenshot of the image
- Replace the image from same folder of the current task you're executing
- Try lowering the `confidence` which is `0.8` by default

## Bugs?

- `create an issue`

Thank you.
