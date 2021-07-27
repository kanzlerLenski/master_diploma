import sys
import codecs

old_line = ""
wr = ""

with codecs.open(sys.argv[1], encoding="utf-8", errors="ignore") as file:
    with open(sys.argv[1] + "_proc", "w", encoding="utf-8") as outp:
        for i, line in enumerate(file):
            if i == 0:
                old_line = line
                wr = line
            else:
                if line[0:15] == old_line[0:15]:
                    wr += " " + line
                    old_line = line
                else:
                    outp.write(wr.replace("\n", "") + "\n")
                    old_line = line
                    wr = line
            
