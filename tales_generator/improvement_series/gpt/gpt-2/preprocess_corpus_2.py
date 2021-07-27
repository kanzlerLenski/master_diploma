import os
import sys
import re

file = open(sys.argv[1], "r", encoding="utf-8").readlines()
# can be improved by setdefault.
file = list(dict.fromkeys(file))
with open(sys.argv[1] + "_cleaned", "w", encoding="utf-8") as outp:
    for i in range(len(file) - 2, -1, -1):
        file[i] = re.sub(r'\.(?=[^ \W\d])', '.\n', file[i])
        file[i] = file[i].replace(": –", ":\n–")
        if file[i+1].startswith(("- ", "— ", "– ")) and file[i+1][2].islower():
            file[i] = file[i].strip() + " " + file.pop(i + 1)
    for string in file:
        if string.strip() != "":
            outp.write(string)