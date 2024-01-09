from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import argparse
import os


def create_vectordb(path_to_docs):
    """_summary_

    Args:
        path_to_docs (_type_): _description_

    Returns:
        _type_: _description_
    """
    loader = TextLoader(path_to_docs)
    docs = loader.load()
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector_db = FAISS.from_documents(documents, embeddings)
    print(f"> vectorized '{path_to_docs}'")
    return vector_db


def save_vectordb(vector_db, output_path):
    """_summary_

    Args:
        vector_db (_type_): _description_
        output_path (_type_): _description_
    """
    vector_db.save_local(output_path)
    print(f"> index saved to '{output_path}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inp",
        type=str,
        help="plain text input document to be vectorized",
        nargs="?",
        default="./data/papers.txt",
    )
    parser.add_argument(
        "--out",
        type=str,
        help="output directory to save the vector DB to",
        nargs="?",
        default="./data/faiss_index",
    )
    args = parser.parse_args()
    vector_db = create_vectordb(path_to_docs=args.inp)
    save_vectordb(vector_db=vector_db, output_path=args.out)
