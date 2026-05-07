from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)

sample = "M A I V M G R"

tokens = tokenizer(sample)
print(tokens)