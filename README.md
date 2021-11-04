# How to Run DIEGOTOM Search Engine
Make sure that each file is within the same directory.

Type`pip install -r requirements.txt` into your shell to install all third-party libraries.

We ran our programs in Microsoft Visual Studio Code.

Execute Invert.py first with `generate_ALL = True` to install all prerequisite caches, dictionaries and posting text files used for query search.

To use the user interface portion, please use Interface.py. A terminal will appear where you will be able to include a free-text query to 
generate a list of relevant documents that are retrieved based on your query.

Interface.py uses functions from Help_func.py, Search.py, and Invert.py

Eval.py returns the mean average precision values for each cache.txt file. It must be run separately.

R-precision returns the R-precision of each cache.txt file. It must be run separately.

# IR System Details