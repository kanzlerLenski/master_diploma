import os
import sys
import codecs

for filename in os.listdir(r"{}".format(sys.argv[1])):
    with codecs.open(sys.argv[1] + "//" + filename, "r",
                     encoding="utf-8", errors="ignore") as file:
        with open(sys.argv[1] + "//" + filename + "_proc", "w",
                  encoding="utf-8") as outp:
            for i, line in enumerate(file):
                if i == 0 or "NULL" in line:
                    pass
                else:
                    line = line.split("\t")
                    outp.write(line[1] + "\n" + line[2] + "\n")
