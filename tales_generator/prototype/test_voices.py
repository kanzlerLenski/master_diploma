import pyttsx3

tts = pyttsx3.init() # Инициализировать голосовой движок.
voices = tts.getProperty('voices')
rate = tts.getProperty('rate')

# Попробовать установить предпочтительный голос

for voice in voices:
    print(voice.name)
    if voice.name == 'Aleksandr':
        tts.setProperty('voice', voice.id)
        tts.setProperty('rate', rate-50)
        
tts.say('Zdrastvuite! Menya zovut Aleksandr. A kak Vashe imya?')
tts.runAndWait()
