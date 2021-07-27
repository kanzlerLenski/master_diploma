import sys
import codecs

with codecs.open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as file:
        with open(sys.argv[1] + "_proc", "w", encoding="utf-8") as outp:
            for i, line in enumerate(file):
                line = line.split()
                if not line[1].isupper():
                    outp.write(" ".join(line[3:]) + "\n")
                else:
                    outp.write(" ".join(line[1:]) + "\n")
