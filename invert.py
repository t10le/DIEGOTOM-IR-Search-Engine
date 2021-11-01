import helper_func as diegotom


with open("cacm.all", "r") as f:
    text = f.read()
    text_split = text.split(".I ")
    sub = text_split[1:]
    # print(sub)


diegotom.pre_processing(text_split)
