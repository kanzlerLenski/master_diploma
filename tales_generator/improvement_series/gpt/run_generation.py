#!/usr/bin/env python3
# coding=utf-8

import argparse
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from nltk import sent_tokenize
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()

objects = ["стол", "стул", "мячик", "человек", "ручка"]
backup = ["Колобок", "Баба", "Яга", "Буратино", "Золушка", "Винни-Пух", "Чебурашка", "Щелкунчик", "Муха-Цокотуха",
          "Принцесса", "Кощей", "Алладин", "Царевна", "Емеля", "Русалочка", "Мойдодыр", "Леший", "Дюймовочка",
          "Белоснежка", "Маугли", "Снегурочка", "Принц", "Водяной", "Незнайка", "Мальвина", "Иван-дурак",
          "Морозко"]
output = ""
stack = []

MAX_LENGTH = int(10000)  # Hardcoded max length to avoid infinite loop


def adjust_length_to_model(length, max_sequence_length):
    if length < 0 and max_sequence_length > 0:
        length = max_sequence_length
    elif 0 < max_sequence_length < length:
        length = max_sequence_length  # No generation bigger than model size
    elif length < 0:
        length = MAX_LENGTH  # avoid infinite loop
    return length


def make_replaces(string):
    tags = ["<beginning>", "</beginning>",
            "<ending>", "</ending>",
            "<start>", "<end>",
            "<title>", "</title>"]
    for tag in tags:
        string = string.replace(tag, "")
    return string


def embed_characters(text):
    text = text.split()
    for i, word in enumerate(text):
        if "<character_" in word:
            word = word.split("_")
            word[-1] = word[-1][:4]
            text[i] = choose_character(word, characters=objects)
    return " ".join(text)


def choose_character(word, characters):
    global stack

    if stack:
        check = [x for (x, y) in stack if y == word[1]]
        if check:
            character = check[0]
            name = morph.parse(character)[0].inflect({word[3], word[4]})[0]
            return name
        else:
            candidate = random.choice(characters)
            if morph.parse(candidate)[0].tag.gender == word[2]:
                name = morph.parse(candidate)[0].inflect({word[3], word[4]})[0]
                stack.append((candidate, word[1]))
                characters.pop(characters.index(candidate))
                return name
            else:
                if any(morph.parse(element)[0].tag.gender == word[2] for element in characters):
                    name = choose_character(word, characters=objects)
                else:
                    name = choose_character(word, characters=backup)
    else:
        candidate = random.choice(characters)
        if morph.parse(candidate)[0].tag.gender == word[2]:
            name = morph.parse(candidate)[0].inflect({word[3], word[4]})[0]
            stack.append((candidate, word[1]))
            characters.pop(characters.index(candidate))
            return name
        else:
            if any(morph.parse(element)[0].tag.gender == word[2] for element in characters):
                name = choose_character(word, characters=objects)
            else:
                name = choose_character(word, characters=backup)
    return name


def make_readable_story(generated_sequences):

    temp = generated_sequences[generated_sequences.rfind(".") + 1:]
    output = generated_sequences + generate("<ending>" + temp, 100)
    output = embed_characters(make_replaces(output))
    return output


def generate(prompt, length=500):

    model_name_or_path = r"C:\Users\Eugene\PycharmProjects\tales_generator\improvement_series\GPT-3\test\test3"
    stop_token = "<end>"

    temperature = 1.0
    repetition_penalty = 1.0
    k = 0
    p = 0.9
    prefix = ""
    num_return_sequences = 1

    # Initialize the model and tokenizer
    
    model_class, tokenizer_class = (GPT2LMHeadModel, GPT2Tokenizer)
        
    tokenizer = tokenizer_class.from_pretrained(model_name_or_path)
    model = model_class.from_pretrained(model_name_or_path)

    length = adjust_length_to_model(length, max_sequence_length=model.config.max_position_embeddings)

    prompt_text = prompt if prompt else input("Model prompt >>> ")

    prefix = prefix
    encoded_prompt = tokenizer.encode(prefix + prompt_text, add_special_tokens=False, return_tensors="pt")

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

    for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
        # print("=== GENERATED SEQUENCE {} ===".format(generated_sequence_idx + 1))
        generated_sequence = generated_sequence.tolist()

        # Decode text
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

        # Remove all text after the stop token
        text = text[: text.find(stop_token)]

        # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
        total_sequence = (
            prompt_text + text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)) :]
        )

        generated_sequences.append(total_sequence)
        # print(total_sequence)

    return " ".join(generated_sequences)

prompt = "В тридевятом царстве, в тридесятом государстве жил-был старик со старухою. И было у них три сына."
print(generate(prompt))
