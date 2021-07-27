import os
import sys
import codecs

for filename in os.listdir(r"{}".format(sys.argv[1])):
    with codecs.open(sys.argv[1] + "//" + filename, "r",
                     encoding="utf-8", errors="ignore") as file:
        with open(sys.argv[1] + "//" + filename + "_proc", "w",
                  encoding="utf-8") as outp:
            for line in file:
                if line.strip() != "":
                    line = line.split()
                    if line[0].endswith(":"):
                       outp.write(" ".join(line[1:]) + "\n")
