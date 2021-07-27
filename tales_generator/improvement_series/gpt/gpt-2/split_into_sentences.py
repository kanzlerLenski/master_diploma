from nltk import sent_tokenize
import os
import sys

def split_into_sents(text):

    split = sent_tokenize(text)
    return split


for filename in os.listdir(r"{}".format(sys.argv[1])):
    file = open(sys.argv[1] + "//" + filename, "r", encoding="utf-8").read()
    with open(sys.argv[1] + "//" + filename + "_split", "w", encoding="utf-8") as outp:
        for line in split_into_sents(file):
            outp.write(line + '\n')
