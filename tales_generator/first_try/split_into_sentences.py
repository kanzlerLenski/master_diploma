from nltk import sent_tokenize

text = open('all_tales_deduped.txt', 'r', encoding='utf-8').read()

def split_into_sents(text):

    split = sent_tokenize(text)
    return split

with open('all_tales_deduped_split.txt', 'w', encoding='utf-8') as outp:
    for line in split_into_sents(text):
        outp.write(line + '\n')
