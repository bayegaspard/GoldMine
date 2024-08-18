import os
import pdfplumber
from bs4 import BeautifulSoup
import markdown
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

PERSIST_DIRECTORY = "/tmp"

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

    def load_pdf(self, file_path):
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text

    def load_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        return soup.get_text()

    def load_md(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            html = markdown.markdown(f.read())
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()

    def load_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def process_and_store_documents(self, files):
        all_pages = []
        for file in files:
            file_path = os.path.join("/tmp", file.filename)
            file.save(file_path)

            if file.filename.endswith('.pdf'):
                content = self.load_pdf(file_path)
            elif file.filename.endswith('.html'):
                content = self.load_html(file_path)
            elif file.filename.endswith('.md'):
                content = self.load_md(file_path)
            elif file.filename.endswith('.txt'):
                content = self.load_txt(file_path)
            else:
                continue

            all_pages.append({"content": content})

        # Store documents in the vectorstore
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
