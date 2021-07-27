import sys
import random

file_len = int(sys.argv[2])
num_lines = int(sys.argv[3])
lines = []

while len(lines) < num_lines:
    lines.append(random.randint(0, file_len))

with open(sys.argv[1] + "_valid", "w", encoding="utf-8") as outp:
    with open(sys.argv[1], "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i in lines:
                outp.write(line)