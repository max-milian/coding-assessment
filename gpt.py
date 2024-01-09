import os
import argparse
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain


def main(query, model, path_to_vectordb):
    llm = ChatOpenAI(model_name=model, openai_api_key=os.getenv("OPENAI_API_KEY"))
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.load_local(path_to_vectordb, embeddings)
    prompt = ChatPromptTemplate.from_template(
        """Answer the following question based only on the provided context:
        <context>
        {context}
        </context>

        Question: {input}"""
    )
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectordb.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": query})
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inp", type=str, help="question to ask the model")

    parser.add_argument(
        "--openai_model",
        type=str,
        help="OpenAI model to use",
        nargs="?",
        default="gpt-3.5-turbo",
    )
    parser.add_argument(
        "--vector",
        type=str,
        help="path to vector DB to retrieve from",
        nargs="?",
        default="./data/faiss_index",
    )
    args = parser.parse_args()

    response = main(
        query=args.inp, model=args.openai_model, path_to_vectordb=args.vector
    )
    print(response["answer"])
