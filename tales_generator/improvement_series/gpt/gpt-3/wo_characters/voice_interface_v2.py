import speech_recognition as sr
import pyttsx3
import pymorphy2
from generate_text_wo_chars import make_readable_story
from generate_text_wo_chars import objects
from dialog import dialog
from akinator import play
import time
import keyboard


def speak(what):
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def tell_story(promt):
    print("Подождите, сказка генерируется.")
    speak("Генерирую сказку.")
    story = make_readable_story(promt)
    print(f"Сказка: {story}")
    speak("Генерация завершена. Приготовьтесь слушать!")
    speak(story)


def read_objects(objects_):
    speak_engine.say("Я вижу:")
    for object_ in objects_:
        speak_engine.say(object_)
    speak("Как бы Вы хотели, чтобы сказка начиналась?")


def listen_and_talk(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print(f"Вы сказали: '{voice}'")

        if "сказк" in voice:
            read_objects(objects)

        elif "поговорить" in voice:
            dialog()

        elif "играть" in voice:
            play()

        elif voice.startswith("пока"):
            speak("До свидания!")
            keyboard.press_and_release('ctrl+c, space')

        else:
            tell_story(voice)

    except sr.UnknownValueError:
        speak("Прошу прощения, команда не распознана. Повторите, пожалуйста!")
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

speak("Здравствуйте! Меня зовут iCub. Я могу рассказать Вам сказку," 
      "поиграть с Вами в игру, в которой Вы загадываете персонажа, а я отгадываю,"
      "или можем просто поговорить. Чем бы Вы хотели заняться?")
r.listen_in_background(m, listen_and_talk)
while True: time.sleep(0.1)
