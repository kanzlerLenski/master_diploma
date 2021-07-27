import pyttsx3

tts = pyttsx3.init() # Инициализировать голосовой движок.
voices = tts.getProperty('voices')
tts.setProperty('voice', 'ru') 

# Попробовать установить предпочтительный голос

tts.say('Командный голос вырабатываю, товарищ генерал-полковник!')
tts.runAndWait()