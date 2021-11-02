import helper_func as diegotom


def makeChanges(flag):
    print("ENTEREDDDD")
    with open("cacm.all", "r") as f:
        text = f.read()
        text_split = text.split(".I ")
        sub = text_split[1:]
        # print(sub)

    # Create document dictionary.
    # {'docID', ['term','term','term']}
    doc_corpus = diegotom.pre_processing(text_split)

    # Create vocabulary dictionary.
    # {'term', ['docID', 'docID']}
    all_terms = diegotom.build_vocab(doc_corpus)

    with open("dictionary.txt", "w") as f:
        f.write(str(doc_corpus))

    with open("postings.txt", "w") as f:
        f.write(str(all_terms))
