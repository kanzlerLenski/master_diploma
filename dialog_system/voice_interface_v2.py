import speech_recognition as sr
import pyttsx3
import pymorphy2
from generate_text_wo_chars import make_readable_story
from generate_text_wo_chars import objects
import dialog_system
import akinator_game
import time
import keyboard

check = True

speak_engine = pyttsx3.init()
r = sr.Recognizer()
m = sr.Microphone(device_index=1)
morph = pymorphy2.MorphAnalyzer()
objects = [morph.parse(word)[0].inflect({"accs"}).word for word in objects]


def speak(what):
   speak_engine.say(what)
   speak_engine.runAndWait()
   speak_engine.stop()


def tell_story(prompt):
    speak("Генерирую сказку.")
    print("iCub: Подождите, сказка генерируется.")
    story = make_readable_story(prompt)
    print(f"iCub: Сказка: {story}")
    speak("iCub: Генерация завершена. Приготовьтесь слушать!")
    speak(story)


def read_objects(objects_):
    speak_engine.say("iCub: Я вижу:")
    global check
    if check == True:
        keyboard.press_and_release('ctrl+c, space')
        check = False
    for object_ in objects_:
        speak_engine.say(object_)
    print("iCub: Я вижу:", " ".join(objects_))
    speak("Как бы Вы хотели, чтобы сказка начиналась?")
    with sr.Microphone() as m:
       voice = recognizer.recognize_google(r.listen(m), language = "ru-RU").lower()
       print("Вы:", voice)
       tell_story(voice)


def listen_and_talk(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("Вы:", voice)

        if "сказк" in voice:
            read_objects(objects)

        elif "поговори" in voice:
            speak("Хорошо. Скажите что-нибудь.")
            print("iCub: Хорошо. Скажите что-нибудь.")
            keyboard.press_and_release('ctrl+c, space')            
            dialog_system.main()
            speak("Чем теперь хотели бы заняться?")
            print("iCub: Чем теперь хотели бы заняться?")

        elif "играть" in voice:
            speak("Хорошо. Загадайте любого персонажа или реального человека, а я постараюсь угадать, кто это."
                  "Отвечайте на мои вопросы 'да', 'нет' или 'не знаю', пожалуйста. Вы также можете попросить меня повторить вопрос.")
            print("iCub: Хорошо. Загадайте любого персонажа или реального человека, а я постараюсь угадать, кто это."
                  "Отвечайте на мои вопросы да и нет, пожалуйста. Вы также можете попросить меня повторить вопрос.")
            keyboard.press_and_release('ctrl+c, space')
            
            akinator_game.main()
            speak("Чем теперь хотели бы заняться?")
            print("iCub: Чем теперь хотели бы заняться?")

        elif voice.startswith("пока"):
            speak("До свидания!")
            print("iCub: До свидания!")
            sys.exit(0)
            
        else:
            speak("Прошу прощения, команда не распознана. Повторите, пожалуйста!")
            print("iCub: Голос не распознан. Повторите, пожалуйста!")
            voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
            keyboard.press_and_release('ctrl+c, space')
            
    except sr.UnknownValueError:
        speak("Прошу прощения, команда не распознана. Повторите, пожалуйста!")
        print("iCub: Голос не распознан. Повторите, пожалуйста!")
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()


speak("Здравствуйте! Меня зовут Айкаб. Я могу рассказать Вам сказку,"
      "поиграть с Вами в игру, в которой Вы загадываете персонажа, а я отгадываю,"
      "или можем просто поговорить. Чем бы Вы хотели заняться?")

# with m as source:
#    r.adjust_for_ambient_noise(source)

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[3].id)

r.listen_in_background(m, listen_and_talk)
while True: time.sleep(0.1)
