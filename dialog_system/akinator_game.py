import akinator
from deep_translator import GoogleTranslator
import speech_recognition as sr
import pyttsx3

aki = akinator.Akinator()

speak_engine = pyttsx3.init()
r = sr.Recognizer()

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[3].id)


def speak(what):
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

    
def translate_answer(a):
    if a == "да":
        a = "y"
    elif a == "нет":
        a = "n"
    elif "не знаю" in a:
        a = "idk"
    elif a == "возможно" or a == "может быть" or a == "частично":
        a = "p"
    elif a == "скорее нет" or a == "не совсем":
        a = "pn"
    return a

    
def game():
    
    q = aki.start_game() # child_mode

    while aki.progression <= 80:

        question = GoogleTranslator(source='en', target='ru').translate(q)

        with sr.Microphone() as m:
        
            try:
                speak(question)
                print("iCub:", question)
                # a = input(question + "\n\t")

                r.adjust_for_ambient_noise(m, duration=0.2)
                voice = r.recognize_google(r.listen(m), language = "ru-RU").lower()
                print("Вы:", voice)
                
                if "повтори" in voice:
                    try:
                        q = aki.back()
                    except akinator.CantGoBackAnyFurther:
                        pass
                else:
                    q = aki.answer(translate_answer(voice))
                    
            except akinator.exceptions.InvalidAnswerError:
                # a = input("Пожалуйста, переформулируйте свой ответ.\n\t")
                speak("Пожалуйста, переформулируйте свой ответ.")
                print("iCub: Пожалуйста, переформулируйте свой ответ.")
                r.adjust_for_ambient_noise(m, duration=0.2)
                voice = r.recognize_google(r.listen(m), language = "ru-RU").lower()
                q = aki.answer(translate_answer(voice))

            except sr.UnknownValueError:
                speak("Прошу прощения, команда не распознана. Повторите, пожалуйста!")
                print("iCub: Голос не распознан. Повторите, пожалуйста!")
                voice = r.recognize_google(r.listen(m), language = "ru-RU").lower()
                q = aki.answer(translate_answer(voice))
                
            question = GoogleTranslator(source='en', target='ru').translate(q)
    aki.win()

    with sr.Microphone() as m:
        correct = f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?\n" # {aki.first_guess['absolute_picture_path']}"
        # correct = input(GoogleTranslator(source='en', target='ru').translate(correct) + "\n\t")
        correct = GoogleTranslator(source='en', target='ru').translate(correct)
        speak(correct)
        print("iCub:", correct)
        r.adjust_for_ambient_noise(m, duration=0.2)
        voice = r.recognize_google(r.listen(m), language = "ru-RU").lower()
        if voice == "да":
            speak("Ура!")
            print("iCub: Ура!")
            return True
        else:
            speak("Хм. Продолжим.")
            print("iCub: Хм. Продолжим.")
            return False


def play():
    while True:
        if game():
            # line = "Сыграем ещё?"
            # ans = input(line + "\n\t")
            speak("Сыграем ещё?")
            print("iCub: Сыграем ещё?")
            with sr.Microphone() as m:
                r.adjust_for_ambient_noise(m, duration=0.2)
                voice = r.recognize_google(r.listen(m), language = "ru-RU").lower()
                print("Вы:", voice)
                if voice == "да":
                    game()
                else:
                    break


def main():
    play()


if __name__ == '__main__':
    main()
