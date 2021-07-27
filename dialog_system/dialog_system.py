from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging
import speech_recognition as sr
import pyttsx3
import sys
from db import db
import random
import pymorphy2
from nltk import word_tokenize

logging.getLogger("transformers").setLevel(logging.CRITICAL)

MAX_LENGTH = int(10000)  # hardcoded max length to avoid infinite loop

speak_engine = pyttsx3.init()
r = sr.Recognizer()

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[3].id)

morph = pymorphy2.MorphAnalyzer()

old_ans = ""

    
def speak(what):
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def adjust_length_to_model(length, max_sequence_length):
    if length < 0 and max_sequence_length > 0:
        length = max_sequence_length
    elif 0 < max_sequence_length < length:
        length = max_sequence_length  # no generation bigger than model size
    elif length < 0:
        length = MAX_LENGTH  # avoid infinite loop
    return length


# generation parameters

def generate(prompt, length=500):
    model_name_or_path = r"C:\Users\Eugene\PycharmProjects\dialog_system\model\small\3_epochs_256"
    stop_token = ""

    temperature = 1.0
    repetition_penalty = 1.2
    num_beams = 0
    do_sample = False
    k = 10
    p = 0.95
    prefix = ""
    num_return_sequences = 1

    # Initialize the model and tokenizer

    model_class, tokenizer_class = (GPT2LMHeadModel, GPT2Tokenizer)

    tokenizer = tokenizer_class.from_pretrained(model_name_or_path)
    model = model_class.from_pretrained(model_name_or_path)

    # a way to move do generation on GPU if enough memory
    # model.to('cuda')

    length = adjust_length_to_model(length,
                                    max_sequence_length=model.config.max_position_embeddings)

    prompt_text = prompt if prompt else input("Model prompt >>> ")

    prefix = prefix
    encoded_prompt = tokenizer.encode(prefix + prompt_text,
                                      add_special_tokens=False,
                                      return_tensors="pt")

    if encoded_prompt.size()[-1] == 0:
        input_ids = None
    else:
        input_ids = encoded_prompt

    output_sequences = model.generate(
        input_ids=input_ids,
        max_length=length + len(encoded_prompt[0]),
        temperature=temperature,
        top_k=k,
        top_p=p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        num_return_sequences=num_return_sequences,
    )

    # Remove the batch dimension when returning multiple sequences
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()

    generated_sequences = []

    for generated_sequence_idx, generated_sequence in \
            enumerate(output_sequences):
        # print("=== GENERATED SEQUENCE {} ===".format
        # (generated_sequence_idx + 1))
        generated_sequence = generated_sequence.tolist()

        # Decode text
        text = tokenizer.decode(generated_sequence,
                                clean_up_tokenization_spaces=True)

        # Remove all text after the stop token
        # text = text[: text.find(stop_token)]

        # Add the prompt at the beginning of the sequence.
        # Remove the excess text that was used for pre-processing
        # total_sequence = (
        #         prompt_text + " " + text[len(tokenizer.decode(
        #             encoded_prompt[0], clean_up_tokenization_spaces=True)):]
        # ) 

        total_sequence = (" " + text[len(tokenizer.decode(
            encoded_prompt[0], clean_up_tokenization_spaces=True)):]
                          )
        generated_sequences.append(total_sequence)

    return " ".join(generated_sequences)


def process_ans(ans_):

    ans_ = " ".join(ans_.split())
    if ans_.startswith("?"):
        ans_ = ans_[1:]
        
    temp = ans_.rfind("\n")
    if temp != -1:
        ans_ = ans_.split("\n")[0]
        
    ans_ = ans_.strip()

    stop = 0
    for i, c in enumerate(ans_):
        if c in (".", "!", "?"):
            stop = i
            break

    if stop != 0:
        ans_ = ans_[:stop+1] 
    
    l = word_tokenize(ans_)
    
    for i, w in enumerate(l):

        if i != 0 and not w.islower() and not w.isupper() \
           and not w[0].isupper():
            for n, c in enumerate(w):
                if c.isupper():
                    if w[n-1].isalpha():
                        l[i] = w[:n] + ". " + w[n:]
                    else:
                        l[i] = w[:n] + " " + w[n:]

        word = morph.parse(w)[0]

        if "я" in l or "Я" in l:
            if word.tag.POS == "VERB" and word.tag.gender == "femn":
                l[i] = word.inflect({"masc"})[0]

        if word.tag.POS == "VERB" and word.tag.person == "2per" and \
            word.tag.number == "sing":
            l[i] = word.inflect({"plur"})[0]

        if w.lower() == "ты":
            l[i] = "Вы"
        elif w.lower() == "тебя":
            l[i] = "Вас"
        elif w.lower() == "тобой":
            l[i] = "Вас"
        elif w.lower() == "твое":
            l[i] = "Ваше"
        elif w.lower() == "тебе":
            l[i] = "Вам"
            
    ans_ = " ".join(l)
    ans_ = ans_.replace(" ?", "?").replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" )", ")")
        
    return ans_


def chat(voice):
    
    global old_ans
    
    if voice in db.keys():
        for key in db:
            if voice in key:
                if type(db[key]) == list:
                    ans = random.choice(db[key])
                else:
                    ans = db[key]
                print("Вы:", voice)
                if ans == "айкаб":
                    print("iCub: iCub.")
                    speak(ans)
                    break
                elif ans == "робот каб проджект":
                    print("iCub: The RobotCub Project.")
                    speak(ans)
                    break
                else:
                    print("iCub:", ans)
                    speak(ans)
                    break

        old_ans = ans
   
    elif "стоп" in voice:
        print("Вы:", voice)
        return

    else:
        print("Вы:", voice)
        # prompt = input()
        print("old_ans", old_ans)
        ans = generate(old_ans + voice + ".", 30)
        if ans.strip() == "":
            generate(voice + ".", 30)
        print("ans:", ans)
        ans = process_ans(ans)
        print("iCub:", ans)
        speak(ans)

        old_ans = ans
                
    
def dialog():
  
    while True:
        with sr.Microphone() as m:
            voice = ""
            try:
                r.adjust_for_ambient_noise(m, duration=0.2)
                voice = r.recognize_google(r.listen(m), language="ru-RU").lower()
            except sr.UnknownValueError:
                if voice == "":
                    speak("iCub: Прошу прощения, повторите, пожалуйста.")
                    voice = r.recognize_google(r.listen(m), language="ru-RU").lower()
                else:
                    chat(voice)
            if "стоп" in voice:
                return
            else:
                chat(voice)


def main():
    dialog()


if __name__ == '__main__':   
    main()
