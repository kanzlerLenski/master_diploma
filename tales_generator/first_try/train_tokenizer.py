from tokenizers import ByteLevelBPETokenizer
import sys

path = sys.argv[1]

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(files=path, vocab_size=50257, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
    "<start>", "<end>",
    "<title>", "</title>",
    "<character_0>", "<character_1>", "<character_2>", "<character_3>", "<character_4>",
    "<beginning>", "</beginning>",
    "<ending>", "</ending>",
])

# Save files to disk
tokenizer.save(".", "new")