import os
import sys


def get_file_info(filename_):
    text_ = open(sys.argv[1] + "//" + filename_, "r", encoding="utf-8").read()
    file_len_ = len(text_.split("\n"))
    beginning_num_ = int(file_len_ * (10 / 100))
    ending_num_ = file_len_ - beginning_num_
    return file_len_, beginning_num_, ending_num_


def annotate(line_num, output_f, file_len_, beginning_num_, ending_num_, tokens_):
    if line_num == 1:
        output_f.write("<beginning> " + " ".join(tokens_) + "\n")
    elif line_num == beginning_num_ + 1:
        output_f.write(" ".join(tokens_) + " " + "</beginning>\n")
    elif line_num == ending_num_:
        output_f.write("<ending> " + " ".join(tokens_) + "\n")
    elif line_num == file_len_ - 2:
        output_f.write(" ".join(tokens_) + " " + "</ending>\n")
        output_f.write("<end>")
    else:
        output_f.write(" ".join(tokens_) + "\n")


for filename in os.listdir(r"{}".format(sys.argv[1])):
    file_len, beginning_num, ending_num = get_file_info(filename)
    with open(sys.argv[1] + "//" + filename, "r", encoding="utf-8") as file:
        with open(sys.argv[1] + "//" + filename + "_annot_wo_chars", "w", encoding="utf-8") as outp:
            outp.write("<start>\n")
            for i, line in enumerate(file):
                line = line.strip()
                if i == 0:
                    line = line.replace("&lt; title &gt;", "<title>").replace("&lt; / title &gt;", "</title>")
                tokens = line.split()
                annotate(i, outp, file_len, beginning_num, ending_num, tokens)
