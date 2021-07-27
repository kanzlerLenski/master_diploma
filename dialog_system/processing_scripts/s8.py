import sys
import codecs

prev_line = ""
new_line = ""

with codecs.open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as file:
        with open(sys.argv[1] + "_proc", "w", encoding="utf-8") as outp:
            for i, line in enumerate(file):
                line = line.strip().split()
                if prev_line == line[0]:
                    new_line += " ".join(line[1:])
                else:
                    if new_line == "":
                        outp.write("\n" + " ".join(line[1:]))
                        prev_line = line[0]
                    else:
                        outp.write(" " + new_line)
                        outp.write("\n" + " ".join(line[1:]))
                        prev_line = line[0]
                        new_line = ""
