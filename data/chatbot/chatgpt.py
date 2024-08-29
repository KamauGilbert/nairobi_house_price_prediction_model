import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain  # Using langchain if class is missing in community package
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader  # Original import
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import Chroma
from langchain.schema import Document  # Ensure you have the Document class

OPENAI_API_KEY = ""

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
    query = sys.argv[1]

# Load the data_path text
data_path = "data.txt"

# Define a custom loader to return Document objects
class UTF8TextLoader(TextLoader):
    def lazy_load(self):
        with open(self.file_path, encoding='utf-8') as f:
            text = f.read()
        # Return a list of Document objects
        return [Document(page_content=text)]

# Use this custom loader instead of the default one
loader = UTF8TextLoader(data_path)

if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))
    index = VectorstoreIndexWrapper(vectorstore=vectorstore)
else:
    if PERSIST:
        index = VectorstoreIndexCreator(
            embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
            vectorstore_kwargs={"persist_directory": "persist"}
        ).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator(
            embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        ).from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []
while True:
    if not query:
        query = input("Prompt: ")
    if query in ['quit', 'q', 'exit']:
        sys.exit()
    result = chain({"question": query, "chat_history": chat_history})
    print(result['answer'])

    chat_history.append((query, result['answer']))
    query = None