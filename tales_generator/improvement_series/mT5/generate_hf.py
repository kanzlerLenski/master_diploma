from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

torch.device("cuda")
path = r"C:/Users/Eugene/PycharmProjects/tales_generator/experiments/improvement_series/mT5/outputs/best_model"

model = AutoModelForSeq2SeqLM.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained(path)
model.to('cuda')

input_str = "Жили-были дед да баба "
input_ids = tokenizer(input_str, return_tensors="pt").input_ids.to('cuda')

print(tokenizer.decode(model.generate(input_ids)[0]))
