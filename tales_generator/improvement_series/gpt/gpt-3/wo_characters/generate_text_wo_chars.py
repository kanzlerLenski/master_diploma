#!/usr/bin/env python3
# coding=utf-8

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pymorphy2
import random
from nltk import FreqDist
import time
import enchant
import torch
import logging

logging.getLogger("transformers").setLevel(logging.CRITICAL)

start_time = time.time()

morph = pymorphy2.MorphAnalyzer()
dictionary = enchant.Dict("ru_RU")

# words that shouldn't be replaced
forbidden = ["доч", "сын", "дед", "матуш", "баб", "отец", "бат", "пап", "отеч",
             "отц", "отч", "брат", "сестр", "мам", "мачех", "вну", "дурак",
             "мат", "молодец", "старший", "кум", "муж", "жена", "друг",
             "дурачок"]

# a list of recognized objects from camera
objects = ["кукла", "мячик", "кот", "собака"]
stack = []
replaces = []

MAX_LENGTH = int(10000)  # hardcoded max length to avoid infinite loop


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
    model_name_or_path = r"C:\Users\Eugene\PycharmProjects\tales_generator\experiments\improvement_series\GPT\GPT-2\ruGPT2Large\model\3_epochs_256"
    stop_token = "<end>"

    temperature = 1.0
    repetition_penalty = 1.0
    num_beams = 0
    do_sample = False
    k = 50
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
                                    max_sequence_length= \
                                    model.config.max_position_embeddings)

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
        text = text[: text.find(stop_token)]

        # Add the prompt at the beginning of the sequence.
        # Remove the excess text that was used for pre-processing
        total_sequence = (
                prompt_text + " " + text[len(tokenizer.decode(
                    encoded_prompt[0], clean_up_tokenization_spaces=True)):]
        )

        generated_sequences.append(total_sequence)

    return " ".join(generated_sequences)

# remove tags from the sequence

def make_replaces(string):
    tags = ["<beginning>", "</beginning>",
            "<ending>", "</ending>",
            "<start>", "<end>",
            "<title>", "</title>", "&quot;"]
    for tag in tags:
        string = string.replace(tag, "")
        
    return string

# get a root from of a word

def normalize(token_):
    return morph.parse(token_.lower())[0].normal_form

# check if a word is an animated noun

def get_tag(token_):
    token_ = ''.join(x for x in token_.lower() if x.isalpha() or x == '=')
    tag = morph.parse(token_)[0].tag
    return tag.POS == "NOUN" and tag.animacy == "anim"

# get a list of characters to be replaced

def get_fdist(tokens):
    normalized = []
    for word in tokens:
        word = ''.join(x for x in word if x.isalpha() or x == "-")
        norm_word = normalize(word)
        if get_tag(norm_word) and norm_word not in forbidden and \
           norm_word not in objects: # check so words won't repeat
            normalized.append(norm_word)
    fdist_ = FreqDist(normalized).most_common(10)

    # check if a word exists (анти-склеивание)
    fdist_ = [word[0] for word in fdist_ if dictionary.check(word[0]) and \
              word[1] >= 2] # > 5

    # check if no relatives defining or alike words are chosen.
    fdist_ = [word for word in fdist_ if not any(token in word for token in \
                                              forbidden)]    
    return fdist_

# choose replacements depending on the gender

def choose_characters(characters):
    for i, character in enumerate(characters):
        gender = morph.parse(character)[0].tag.gender
        candidates = [x for x in objects if \
                      morph.parse(x)[0].tag.gender == gender]
        if candidates:
            candidate = random.choice(candidates)
            stack.append(character)
            replaces.append(candidate)
            characters.pop(i)
            objects.pop(objects.index(candidate))
        else:
            characters.pop(i)

# insert new characters

def embed_characters(text):
    text = text.replace(".", ". ").replace("!", "! ").replace("?", "? ").replace("^", "")
    tokens = text.split()
    characters = get_fdist(tokens)
    while characters:
        choose_characters(characters)
    if stack:
        for i, word in enumerate(tokens):
            word = ''.join(x for x in word if x.isalpha() or x == "-")
            norm_word = normalize(word)
            if norm_word in stack:
                idx = stack.index(norm_word)
                tag = morph.parse(word)[0].tag
                tokens[i] = morph.parse(replaces[idx])[0].inflect(
                    {tag.number, tag.case})[0]
    return " ".join(tokens)


# main function for generation and editing

def make_readable_story(prompt):
    from_prompt = [normalize(''.join(x for x in word.lower() if x.isalpha() or \
                                     x == "-")) for word in prompt.split() \
                   if get_tag(word)]
    forbidden.extend(from_prompt)
    text = generate("<beginning> " + prompt + " </beginning> ", 200)
    # text = generate(prompt, 170)
    # text = generate(prompt, 350)
    main_part = text[:text.rfind(".") + 1]
    temp = text[text.rfind(".") + 1:] 
    ending = generate(main_part + " <ending> " + temp, 50)
    output = ending[:ending.rfind(".") + 1]
    output = embed_characters(make_replaces(output))
    # output = embed_characters(make_replaces(main_part))
    return output


# prompt = "В тридевятом царстве в тридесятом государстве жили-были старик со старухой."
# print(make_readable_story(prompt))
# print(stack)
# print(replaces)

# time taken
# print("The generation took: ", round((time.time() - start_time) / 60, 2),
#        "minutes.")
