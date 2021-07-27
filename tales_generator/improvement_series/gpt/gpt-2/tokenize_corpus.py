from sacremoses import MosesTokenizer
import sys
import os

mt = MosesTokenizer(lang='ru')

for filename in os.listdir(r"{}".format(sys.argv[1])):
    file = open(sys.argv[1] + "//" + filename, "r", encoding="utf-8").readlines()
    with open(sys.argv[1] + "//" + filename + "_tokenized", "w", encoding="utf-8") as outp:
        for line in file:
            line = mt.tokenize(line.strip())
            outp.write(' '.join(line) + '\n')