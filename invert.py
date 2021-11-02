import helper_func as diegotom


with open("cacm.all_test", "r") as f:
    text = f.read()
    text_split = text.split(".I ")
    sub = text_split[1:]
    # print(sub)


doc_corpus = diegotom.pre_processing(text_split)
all_terms = diegotom.build_vocab(doc_corpus)
