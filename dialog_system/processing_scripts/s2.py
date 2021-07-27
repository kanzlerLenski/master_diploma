import os
import sys
from nltk import word_tokenize
import codecs

check = False

for filename in os.listdir(r"{}".format(sys.argv[1])):
    with codecs.open(sys.argv[1] + "//" + filename, "r",
                     encoding="utf-8", errors="ignore") as file:
        with open(sys.argv[1] + "//" + filename + "_proc", "w",
                  encoding="utf-8") as outp:
            for i, line in enumerate(file):
                if i in (0, 1):
                    pass
                elif i in (2, 3):
                    if not line.strip().endswith(":"):
                        if check:
                            if line.strip() != "":
                                line = line.split()
                                if not line[0].endswith(":"):
                                    check = True
                                    outp.write(" ".join(line) + "\n")
                        else:
                            pass
                    else:
                        check = True
                elif "Hear the whole conversation." in line:
                    pass
                else:
                    if line.strip() != "":
                        line = line.split()
                        if not line[0].endswith(":"):
                            check = True
                            outp.write(" ".join(line) + "\n")
