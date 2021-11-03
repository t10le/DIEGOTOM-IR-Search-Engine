"""
This program is intended to run manually by the user to create a cache text file
containing the document and posting dictionaries, relative to the user's choice
for turning on/off Stopword and Porter stemming.
"""
import helper_func as diegotom


# --- ONLY MODIFY THESE VALUES IN THIS FILE ---
# Set the flags according to how you want the
# dictionary and postings files be filtered.
#
# True -> Apply filter.
# False -> Do not apply filter.

stopflag = True
stemflag = True

# Loop through the program to generate all cache
# versions(cycles the stop and stem flags).
#
# True -> Generate all cache versions.
# False -> Generate only one cache version,
#          relative to flag settings above.
generate_ALL = False
# ---------------------------------------------


with open("cacm.all_one", "r") as f:
    text = f.read()
    text_split = text.split(".I ")

if generate_ALL:
    cache_versions = [(False, False),
                      (True, False),
                      (False, True),
                      (True, True)]
    cache_titles = ['cache-0-0.txt',
                    'cache-1-0.txt',
                    'cache-0-1.txt',
                    'cache-1-1.txt']

    for i in range(4):
        diegotom.set_flags(
            stop=cache_versions[i][0], stem=cache_versions[i][1])
        doc_corpus = diegotom.pre_processing(text_split)
        all_terms = diegotom.build_vocab(doc_corpus)
        with open(cache_titles[i], "w") as f:
            f.write(str(doc_corpus) + '/diegotom/' + str(all_terms))

else:
    # Step i) Set the Stopword and Porter stemming flags prior to creating the dictionaries.
    diegotom.set_flags(stop=stopflag, stem=stemflag)

    # Step ii) Create document dictionary.
    # Example: {'docID', ['term','term','term']}
    doc_corpus = diegotom.pre_processing(text_split)

    # Step iii) Create vocabulary dictionary.
    # Example: {'term', ['docID', 'docID']}
    all_terms = diegotom.build_vocab(doc_corpus)

    # Step iv) Create a cache textfile with both the dictionary and postings inside.
    if not stopflag and not stemflag:
        filename = "cache-0-0.txt"
    elif stopflag and not stemflag:
        filename = "cache-1-0.txt"
    elif not stopflag and stemflag:
        filename = "cache-0-1.txt"
    elif stopflag and stemflag:
        filename = "cache-1-1.txt"
    else:
        filename = "error_pls_delete_this_file"

    with open(filename, "w") as f:
        f.write(str(doc_corpus) + '/diegotom/' + str(all_terms))
