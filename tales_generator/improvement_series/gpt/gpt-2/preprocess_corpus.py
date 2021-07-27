from nltk import sent_tokenize
from sacremoses import MosesTokenizer
import sys

text = open(sys.argv[1], "r", encoding="utf-8")

mt = MosesTokenizer(lang="ru")
english = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:/\\_@-"

with open(sys.argv[1] + "_tokenized", "w", encoding="utf-8") as outp:
    for line in text:
        line = line.strip()
        if "<doc id=" in line:
            continue
        elif line == "":
            continue
        elif "* * *" in line:
            continue
        elif len(line) < 10:
            continue
        elif line.count(".") > 3:
            continue
        elif line in english:
            continue
        split_sent = sent_tokenize(line)
        for sent in split_sent:
            new_line = mt.tokenize(sent)
            outp.write(" ".join(new_line) + "\n")