from nltk.probability import FreqDist
import pymorphy2
import os
import sys

fdist = FreqDist()
morph = pymorphy2.MorphAnalyzer()


def get_file_info(filename_):
    text_ = open(sys.argv[1] + "//" + filename_, "r", encoding="utf-8").read()
    file_len_ = len(text_.split("\n"))
    beginning_num_ = int(file_len_ * (10 / 100))
    ending_num_ = file_len_ - beginning_num_
    return file_len_, beginning_num_, ending_num_


def get_fdist(filename_):
    text_ = open(sys.argv[1] + "//" + filename_, "r", encoding="utf-8").read().split()
    normalized = []
    for word in text_:
        if get_tag(word) == "NOUN":
            normalized.append(normalize(word))
    fdist_ = FreqDist(normalized).most_common(5)
    fdist_ = [word[0] for word in fdist_]
    return fdist_


def annotate(line_num, output_f, file_len_, beginning_num_, ending_num_, tokens_):
    if line_num == beginning_num_:
        output_f.write("<beginning> ")
        output_f.write(" ".join(tokens_) + "\n")
    elif line_num == beginning_num_ + 3:
        output_f.write(" ".join(tokens_) + " ")
        output_f.write("</beginning>\n")
    elif line_num == ending_num_:
        output_f.write("<ending> ")
        output_f.write(" ".join(tokens_) + "\n")
    elif line_num == file_len_ - 2:
        output_f.write(" ".join(tokens_) + " ")
        output_f.write("</ending>\n")
        output_f.write("<end>")
    else:
        output_f.write(" ".join(tokens_) + "\n")


def if_anim(token_):
    return morph.parse(token_)[0].tag.animacy == "anim"


def normalize(token_):
    return morph.parse(token_.lower())[0].normal_form


def get_tag(token_):
    return morph.parse(token_)[0].tag.POS


for filename in os.listdir(r"{}".format(sys.argv[1])):
    file_len, beginning_num, ending_num = get_file_info(filename)
    fdist = get_fdist(filename)
    stack = [1]
    with open(sys.argv[1] + "//" + filename, "r", encoding="utf-8") as file:
        with open(sys.argv[1] + "//" + filename + "_annot_with_gender", "w", encoding="utf-8") as outp:
            outp.write("<start>\n")
            for i, line in enumerate(file):
                line = line.strip()
                if i == 0:
                    line = line.replace("&lt; title &gt;", "<title>").replace("&lt; / title &gt;", "</title>")
                tokens = line.split()
                for i_t, token in enumerate(tokens):
                    norm_form = normalize(token)
                    if norm_form in fdist and if_anim(token):
                        number = morph.parse(token)[0].tag.number
                        case = morph.parse(token)[0].tag.case
                        gender = morph.parse(token)[0].tag.gender
                        if norm_form in stack:
                            tokens[i_t] = "<character_" + str(stack.index(norm_form) - 1) + f"_{gender}_{number}_{case}>"
                        else:
                            tokens[i_t] = "<character_" + str(len(stack) - 1) + f"_{gender}_{number}_{case}>"
                            stack.append(norm_form)
                annotate(i, outp, file_len, beginning_num, ending_num, tokens)
