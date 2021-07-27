import sys
from deep_translator import GoogleTranslator

with open(sys.argv[1], encoding="utf-8") as file:
    with open(sys.argv[1] + "2_ru", "w", encoding="utf-8") as outp:
        for i, line in enumerate(file):
            if i < 307615:
                pass
            elif line.strip() == "":
                pass
            elif line.strip() == ".":
                pass
            elif line.strip().isdigit():
                outp.write(line + "\n")
            else:
                try:
                    outp.write(GoogleTranslator(source='en', target='ru').translate(line) + "\n")
                except TypeError:
                    pass
