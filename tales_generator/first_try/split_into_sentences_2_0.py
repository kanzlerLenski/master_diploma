import os
import sys
import re

for filename in os.listdir(r"{}".format(sys.argv[1])):
    new_file = []
    file = open(sys.argv[1] + "//" + filename, "r", encoding="utf-16").readlines()
    with open(sys.argv[1] + "//" + filename + "_split", "w", encoding="utf-8") as outp:
        for i in range(len(file) - 2, -1, -1):
            file[i] = re.sub(r'\.(?=[^ \W\d])', '.\n', file[i])
            file[i] = file[i].replace(": –", ":\n–")
            if file[i+1].startswith("- ") and file[i+1][2].islower():
                file[i] = file[i].strip() + " " + file.pop(i + 1)
        for string in file:
            outp.write(string)