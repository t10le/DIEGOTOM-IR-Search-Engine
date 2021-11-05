# DIEGOTOM Information Retrieval Search Engine
DIEGOTOM™ is a search engine that uses vector-space model to retrieve the top-K documents relative to the user's free-text query by using cosine similarity caclulations. The databse used for retrieval is the official CACM collection, `cacm.all`, which contains 3204 documents and 10446 terms.

## Installation
1. Navigate to a directory on your computer you wish to install the above files.
```bash
cd Desktop; mkdir DIEGOTOM_SEARCH_ENGINE; cd DIEGOTOM_SEARCH_ENGINE
```

2. Clone our repo to your directory.
```bash
git init; git clone https://github.com/t10le/DIEGOTOM-IR-Search-Engine.git
```

3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install our third-party libraries mandatory for our search engine.
```bash
pip install -r requirements.txt
```

4. Run the following command to execute our program, then follow the prompted terminal instructions.
```bash
python interface.py
```

5. Enjoy our search engine! :)

into your shell to install all third-party libraries.

We ran our programs in Microsoft Visual Studio Code.

Execute Invert.py first with `generate_ALL = True` to install all prerequisite caches, dictionaries and posting text files used for query search.

To use the user interface portion, please use Interface.py. A terminal will appear where you will be able to include a free-text query to 
generate a list of relevant documents that are retrieved based on your query.

Interface.py uses functions from Help_func.py, Search.py, and Invert.py
Eval.py returns the mean average precision values for each cache.txt file. It must be run separately.
R-precision returns the R-precision of each cache.txt file. It must be run separately.

## File Legend
Main files (in order of dependency):
| File | Description | Technical Notes |
|---| ---| ---|
helper_func.py  | The helper functions that will be used universally across all the programs below 
invert.py       | Creates the cache-x-x.txt files and metadata.txt with either complete automated or single-file generation | The cache-x-x.txt files dictate whether stopword removal and/or Porter Stemming was applied to the database. Hence, the variation.
search.py       | The search ranking algorithm using vector-space model and cosine similarity calculations | search.py depends on ALL cache-x-x.txt, metadata.txt, and cacm.all in order to work.
interface.py    | The terminal-style user interface of the search engine program. | interface.py uses functions from help_func.py, invert.py, and search.py.  
eval.py         | Returns the MAP(Mean Average Precision) score for each cache-x-x.txt file.    | eval.py must be run manually and separately.
R-precision.py  | Returns the R-precision of each cache-x-x.txt file.                           | R-precision.py must be run manually and separately.

## IR System Details
- We assumed that W=TF*IDF ; the weight of a term in the query and document vectors are equal to the term frequency times the term frequency-inverse.
- Vector length normalization is applied to both the query and document vectors.
- Word tokenization and removal of non-alphanumeric characters is applied to both the query and document corpus by default.
- Stopword removal and Porter stemming applied to both the query and document corpus is optionally applied, as instructed by terminal welcome prompt.
- Query will return top-K results, where K=10.
- Average retrieval time is 0.01 seconds.