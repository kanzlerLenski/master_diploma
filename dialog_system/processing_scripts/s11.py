import sys
import json

questions = []
answers = []

with open(sys.argv[1], encoding="utf-8") as json_file:
    data = json.load(json_file)

    for i in range(0,50000):
        try:
            questions.append(data["data"][0]["paragraphs"][i]["qas"][0]["question"])
            answers.append(data["data"][0]["paragraphs"][i]["qas"][0]["answers"][0]["text"])
        except IndexError:
            print(i)
            break
            
with open(sys.argv[1] + "_proc", "w", encoding="utf-8") as outp:
    for n, q in enumerate(questions):
        outp.write(q + "\n")
        outp.write(answers[n] + "\n")
