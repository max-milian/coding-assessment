# coding-assessment

A GPT-powered question-answering-system that retrieves its answers from a knowledge database consisting of arxiv papers about the topic of Llama-2.
The project is based on the [LangChain Framework](https://python.langchain.com/docs/get_started/introduction).

## How to use

1. Setup a python-environment

2. set the OpenAI API key by `export OPENAI_API_KEY='[key]'`.

3. Install the required packages via `pip install -r requirements.txt`

4. Fetch the plain text documents using the arxiv-API by running `python fetch_papers.py` from within the repository's main directory. The following optional arguments can be used (omitting an argument returns the respective default value):

* `--url`: Arxiv-url to fetch. Defaults to `http://export.arxiv.org/api/query?search_query=ti:llama&start=0&max_results=70`
* `--out`: Path to save the fetched documents to. Defaults to `./data/papers.txt`.

5. Create the Vector-Database of the fetched documents by running `python create_vectordb.py` from within the repository's main directory. For creating the embeddings, OpenAI embeddings are used. For the database, FAISS is used. The following optional arguments can be used (omitting an argument returns the respective default value):

* `--inp`: Path to the plain text documents. Defaults to `./data/papers.txt`.
* `--out`: Path to save the vector-Database (index) to. Defaults to `./data/faiss_index`.

6. Query the LLM, taking the context from the fetched documents into account by running `python gpt.py '[query]'` from within the repository's main directory. Replace `[query]` with the actual question. The following optional arguments can be used (omitting an argument returns the respective default value):

* `--openai_model`: OpenAI model to be used. Defaults to `gpt-3.5-turbo`.
* `--vector`: Vector-Database to retrieve from. Defaults to `"./data/faiss_index"`.