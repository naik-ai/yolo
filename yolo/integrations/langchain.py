import os
import bs4
from langchain import hub
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

API_KEY = os.environ["NAIK_OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)


def chat_with_gpt3_5(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message["content"]


if __name__ == "__main__":
    user_message = "What is the capital of France?"
    response_message = chat_with_gpt3_5(user_message)
    print("GPT-3.5 says:", response_message)

# llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=API_KEY)
# loader = WebBaseLoader(
#     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
#     bs_kwargs=dict(
#         parse_only=bs4.SoupStrainer(
#             class_=("post-content", "post-title", "post-header")
#         )
#     ),
# )


# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)


# def pipeline(question):

#     docs = loader.load()
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     splits = text_splitter.split_documents(docs)
#     vectorstore = Chroma.from_documents(
#         documents=splits, embedding=OpenAIEmbeddings(api_key=API_KEY)
#     )
#     retriever = vectorstore.as_retriever()
#     prompt = hub.pull("rlm/rag-prompt")
#     llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

#     rag_chain = (
#         {"context": retriever | format_docs, "question": RunnablePassthrough()}
#         | prompt
#         | llm
#         | StrOutputParser()
#     )
#     return rag_chain.invoke(f"{question}")
