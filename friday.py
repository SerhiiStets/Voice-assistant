#!/usr/bin/env python3

# Requires Pygame, gtts, pyttsx
# For windows: Speech Recognition, PyAudio

import os.path
import random
import webbrowser
import socket
import pyttsx
import logging
import speech_recognition as sr
from sys import platform
from time import sleep, strftime
from pygame import mixer, time
from gtts import gTTS


def internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        logging.exception(e)
        return False


def greetings():
    day_time = int(strftime('%H'))

    if random.random() < 0.5:
        speak("At your service sir")
    else:
        if day_time < 12:
            speak('Good morning')
        elif 12 <= day_time < 18:
            speak('Good afternoon')
        else:
            speak('Good evening')


def speak(audio_string):
    voice_path = "lib/voice/"
    mixer.pre_init(24000, -16, 1, 512)

    def speak_no_internet(audio):
        engine = pyttsx.init()
        engine.say(audio)
        engine.runAndWait()

    def new_audio(name, audio):
        tts = gTTS(text=audio, lang='en-us', slow=False)
        tts.save(voice_path + name)
        speak(audio)

    audio_name = audio_string.lower().replace(" ", "_") + ".mp3"

    if os.path.isfile(voice_path + audio_name):
        mixer.init()
        mixer.music.load(voice_path + audio_name)
        mixer.music.play()
        while mixer.music.get_busy():
            time.Clock().tick(10)
        print(audio_string)
    else:
        if internet_connection():
            new_audio(audio_name, audio_string)
        else:
            speak_no_internet(audio_string)


def listen(recognizer, audio):
    try:
        print(recognizer.recognize_google(audio).capitalize())
        brain(recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("I don't understand")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def brain(request):
    if "where is" in request.lower():
        place = request.replace("?", "").split(" ", 2)
        if len(request.split()) == 3:
            speak("Here's what i found")
            webbrowser.open("https://www.google.com/maps/place/" + place[2] + "/&amp")
        else:
            speak("Please enter place")
    elif "what time is it" in request.lower():
        print(strftime('%H:%M'))


def windows():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)

    r.listen_in_background(m, listen)
    while True:
        sleep(0.1)


def linux():
    while True:
        brain(input())


def main():
    sleep(1)
    greetings()
    if platform.startswith('linux'):
        linux()
    elif platform.startswith('win32'):
        windows()


if __name__ == '__main__':
    main()
