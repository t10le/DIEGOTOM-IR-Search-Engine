import ast
with open('cache.txt', 'r') as f:
    text = f.read()
    delim = text.find('/diegotom/')
    document_dict = text[:delim]
    vocab_dict = text[delim+10:]

document_dict = ast.literal_eval(document_dict)
vocab_dict = ast.literal_eval(vocab_dict)

print(document_dict['1'])
