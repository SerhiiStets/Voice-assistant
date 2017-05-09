#!/usr/bin/env python3

import os.path
import random
import datetime
from pygame import mixer
from pygame import time
from gtts import gTTS


def greetings():
    hours = datetime.datetime.now().hour

    if random.randint(1, 10) < 6:
        speak("At your service sir")
    else:
        if hours < 12:
            speak('Good morning')
        elif 12 <= hours < 18:
            speak('Good afternoon')
        else:
            speak('Good evening')


def speak(audio_string):
    voice_path = "lib/voice/"
    mixer.pre_init(24000, -16, 1, 512)

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
        new_audio(audio_name, audio_string)


def main():
    greetings()


if __name__ == '__main__':
    main()
