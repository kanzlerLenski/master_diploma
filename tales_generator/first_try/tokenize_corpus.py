from sacremoses import MosesTokenizer
import sys

text = open(sys.argv[1], 'r', encoding='utf-8')

mt = MosesTokenizer(lang='ru')



with open(sys.argv[1] + '_tokenized', 'w', encoding='utf-8') as outp:

    for line in text:
        line = mt.tokenize(line.strip())
        outp.write(' '.join(line) + '\n')

