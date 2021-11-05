# DIEGOTOM Information Retrieval Search Engine
DIEGOTOM™ is a search engine that uses vector-space model to retrieve the top-K documents relative to the user's free-text query by using cosine similarity caclulations. The databse used for retrieval is the official CACM collection, `cacm.all`, which contains 3204 documents and 10446 terms.

## Installation
1. Navigate to a directory on your computer you wish to install the above files.
<br>Note: Command-line examples below assumes Mac OSX.
```bash
cd ~/Desktop
```
<br>

2. Clone our repo to your directory.
```bash
git clone https://github.com/t10le/DIEGOTOM-IR-Search-Engine.git; cd DIEGOTOM-IR-Search-Engine
```
<br>

3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install our third-party libraries mandatory for our search engine.
```bash
pip install -r requirements.txt
```
If <strong>ModuleNotFound: Error: No module named</strong> `x` occurs, do the following for the `x` module. 
<br>For nltk example,
```bash
python3 -m pip install nltk
```
<br>

4. Run the following command to execute our program, then follow the prompted terminal instructions.
```bash
python interface.py
```
<br>

5. Enjoy our search engine! :)


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
