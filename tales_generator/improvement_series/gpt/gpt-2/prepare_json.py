import sys
import os

path = r"C:\Users\Eugene\PycharmProjects\tales_generator\improvement_series\validation\tales\split\split_2\tokenized\annot_with_gender"
with open(r"C:\Users\Eugene\Desktop\tales.txt_tokenized_cleaned_annot_valid.json",
          "a", encoding="utf-8") as outp:
    for filename in os.listdir(r"{}".format(path)):
        file = open(path + "//" + filename, "r",
                    encoding="utf-8").read().replace("\n", "")
        outp.write('{"text": "{' + file + '}"}\n')
        
