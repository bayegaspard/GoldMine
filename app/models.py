import os
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma

PERSIST_DIRECTORY = "/path/to/persistent/storage"

class LLMModel:
    def __init__(self, model_name="llama3"):
        self.model, self.embeddings = self.get_model_and_embeddings(model_name)

    def get_model_and_embeddings(self, model_name):
        model = Ollama(model=model_name)
        embeddings = OllamaEmbeddings(model=model_name)
        return model, embeddings

    def create_vector_store(self):
        if not os.path.exists(PERSIST_DIRECTORY):
            os.makedirs(PERSIST_DIRECTORY)
        return Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=self.embeddings)

class DocumentHandler:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def process_and_store_documents(self, files):
        all_pages = []
        for file in files:
            if file.filename.endswith('.pdf'):
                file_path = os.path.join("/tmp", file.filename)
                file.save(file_path)
                loader = PyPDFLoader(file_path)
                pages = loader.load_and_split()
                all_pages.extend(pages)

        self.vectorstore.add_documents(documents=all_pages)
        return self.vectorstore.as_retriever()

class QuestionAnswering:
    def __init__(self, model, prompt_template):
        self.model = model
        self.prompt_template = prompt_template

    def generate_response(self, context, question):
        chain_input = {"context": context, "question": question}
        response = self.prompt_template.format(**chain_input)
        return self.model.invoke(response)
