import speech_recognition as sr
import pyttsx3
import pymorphy2
from generate_text import make_readable_story
from generate_text import objects
import time
import sys


def speak(what):
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def tell_story(promt):
    story = make_readable_story(promt, True)
    print(f"Сказка: {story}")
    speak(story)


def read_objects(objects_):
    speak_engine.say(f"Я вижу:")
    for object_ in objects_:
        speak_engine.say(object_)
    speak("Как бы Вы хотели, чтобы сказка начиналась?")


def listen_and_talk(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print(f"Вы сказали: '{voice}'")

        if voice.startswith("расскажи сказку"):
            read_objects(objects)


        elif voice.startswith("стоп"):
            sys.exit()

        else:
            tell_story(voice)

    except sr.UnknownValueError:
        print("Голос не распознан. Повторите, пожалуйста!")

speak_engine = pyttsx3.init()
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)
morph = pymorphy2.MorphAnalyzer()
objects = [morph.parse(word)[0].inflect({"accs"}).word for word in objects]

#with m as source:
#    r.adjust_for_ambient_noise(source)

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[3].id)

r.listen_in_background(m, listen_and_talk)
while True: time.sleep(0.1)
