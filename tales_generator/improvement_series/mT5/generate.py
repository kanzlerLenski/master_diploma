from simpletransformers.t5 import T5Args, T5Model

path = r"C:\Users\Eugene\PycharmProjects\tales_generator\experiments\improvement_series\mT5\model\3_epochs_350"

model_args = T5Args()
model_args.use_multiprocessed_decoding = False
model_args.do_sample = True
model_args.max_length = 250
model_args.top_k = 0
model_args.top_p = 0.95
model_args.num_return_sequences = 1

model = T5Model("mt5", path, use_cuda=True, args=model_args)
prompt = "В тридевятом царстве в тридесятом государстве жили-были старик со старухой. "
predicts = model.predict([prompt])
print(prompt)
for item in predicts:
    print(item)
