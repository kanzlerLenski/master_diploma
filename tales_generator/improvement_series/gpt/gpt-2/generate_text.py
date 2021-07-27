from transformers import AutoTokenizer, GPT2LMHeadModel
from nltk import sent_tokenize
import pymorphy2
import random

tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\Eugene\PycharmProjects\tales_generator\experiments\improvement_series\GPT-2\training\tales\with_gender\classics\checkpoint-1930000")
model = GPT2LMHeadModel.from_pretrained(r"C:\Users\Eugene\PycharmProjects\tales_generator\experiments\improvement_series\GPT-2\training\tales\with_gender\classics")

#tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\Eugene\PycharmProjects\tales_generator\data_preprocessing\check")
#model = GPT2LMHeadModel.from_pretrained(r"C:\Users\Eugene\PycharmProjects\tales_generator\data_preprocessing\check")

morph = pymorphy2.MorphAnalyzer()

objects = ["стол", "стул", "мячик", "человек", "ручка"]
backup = ["Колобок", "Баба", "Яга", "Буратино", "Золушка", "Винни-Пух", "Чебурашка", "Щелкунчик", "Муха-Цокотуха",
          "Принцесса", "Кощей", "Алладин", "Царевна", "Емеля", "Русалочка", "Мойдодыр", "Леший", "Дюймовочка",
          "Белоснежка", "Маугли", "Снегурочка", "Принц", "Водяной", "Незнайка", "Мальвина", "Иван-дурак",
          "Морозко"]
output = ""
stack = []

def generate(input_context):
    input_ids = tokenizer.encode(input_context, return_tensors="pt")  # encode input context
    outputs = model.generate(input_ids=input_ids, max_length=256, do_sample=True)
    all_tokens = tokenizer.convert_ids_to_tokens(outputs[0].tolist())
    prompt = tokenizer.decode(tokenizer.convert_tokens_to_ids(all_tokens))
    return prompt


def make_replaces(string):
    tags = ["<beginning>", "</beginning>",
            "<ending>", "</ending>",
            "<start>", "<end>",
            "<title>", "</title>"]
    for tag in tags:
        string = string.replace(tag, "")
    return string

# def embed_characters(text):
#   for i in range(6):
#       character_id = f"<character_{i}>"
#       if character_id in text:
#           text = text.replace(character_id, objects[i])
#   return text


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


def make_readable_story(prompt_, flag):
    global output

    if flag:
        output = ""

    while len(output) < 600:
        temp = generate(prompt_)
        temp = sent_tokenize(temp.rsplit('.', 1)[0] + ".")
        output += '\n'.join(temp[:-1])
        make_readable_story(temp[-1], False)

    output = embed_characters(make_replaces(output))
    return output

prompt = "В тридевятом царстве, в тридесятом государстве жил-был старик со старухою. И было у них три сына."
print(make_readable_story(prompt, True))
