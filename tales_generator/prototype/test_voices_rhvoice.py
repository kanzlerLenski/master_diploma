import speechd

tts_d = speechd.SSIPClient('test')
tts_d.set_output_module('rhvoice')
tts_d.set_language('ru')
tts_d.set_rate(50)
tts_d.set_punctuation(speechd.PunctuationMode.SOME)
tts_d.speak('И нежный вкус родимой речи так чисто губы холодит')
tts_d.close()