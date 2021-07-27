import speech_recognition as sr
import pyttsx3
import pymorphy2
from generate_text_wo_chars import make_readable_story
from generate_text_wo_chars import objects
import time
import sys
import keyboard
import threading
from pygame import mixer

check = True
mixer.init()
mixer.music.load('hello.mp3')

def dumd_func():
    print("herehere")
    r.adjust_for_ambient_noise(m, duration=0.3)
    voice = r.recognize_google(r.listen(m), language="ru-RU").lower()
    if any(x in voice for x in ("хватит", "другую", "стоп")):
        mixer.music.stop()
        read_objects(objects)
    
def speak(what):
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()
 

def tell_story(promt):
    print("Подождите, сказка генерируется.")
    speak("Генерирую сказку.")
    # story = make_readable_story(promt)
    story = "расцветали яблони и груши поплыли туманы над рекой выходила на берег катюша на высокий берег на крутой, \
расцветали яблони и груши поплыли туманы над рекой выходила на берег катюша на высокий берег на крутой, \
расцветали яблони и груши поплыли туманы над рекой выходила на берег катюша на высокий берег на крутой \
    расцветали яблони и груши поплыли туманы над рекой выходила на берег катюша на высокий берег на крутой"
    print(f"Сказка: {story}")
    speak("Генерация завершена. Приготовьтесь слушать!")
    #process = threading.Thread(target=speak, args=(story,)).start()
    try:
        mixer.music.play()
    except KeyboardInterrupt:
        mixer.music.stop()
    #try:
    #    process = threading.Thread(mixer.music.play()).start()
    #except KeyboardInterrupt:
    #    mixer.music.stop()
    #process_2 = threading.Thread(target=listen_and_talk).start()

def read_objects(objects_):
    speak_engine.say("Я вижу:")
    global check
    if check == True:
        keyboard.press_and_release('ctrl+c, space')
        check = False
    for object_ in objects_:
        speak_engine.say(object_)
    speak("Как бы Вы хотели, чтобы сказка начиналась?")


def listen_and_talk(recognizer, audio):
    print("here")
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"Вы сказали: '{voice}'")

        if "сказк" in voice:
            read_objects(objects)

        if any(x in voice for x in ("хватит", "другую", "стоп")):
            mixer.music.stop()
            read_objects(objects)
            

        elif voice.startswith("выход"):
            keyboard.press_and_release('ctrl+c, space')

        else:
            tell_story(voice)

    except sr.UnknownValueError:
        speak("Прошу прощения, команда не распознана. Повторите, пожалуйста!")
        global check
        if check == True:
            keyboard.press_and_release('ctrl+c, space')
        check = False
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
