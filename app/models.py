import os
import pdfplumber
from bs4 import BeautifulSoup
import markdown
import docx
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from werkzeug.utils import secure_filename 

UPLOAD_DIRECTORY = "/tmp/uploaded_documents"
PERSIST_DIRECTORY = "/tmp/chroma_persist"

class LLMModel:
    def __init__(self, model_name="llama3"):
        self.model, self.embeddings = self.get_model_and_embeddings(model_name)
        if self.model is None:
            raise ValueError(f"Failed to initialize model {model_name}")

    def get_model_and_embeddings(self, model_name):
        try:
            model = Ollama(model=model_name)
            embeddings = OllamaEmbeddings(model=model_name)
            return model, embeddings
        except Exception as e:
            print(f"Error initializing model: {e}")
            return None, None

    def create_vector_store(self):
        if not os.path.exists(PERSIST_DIRECTORY):
            os.makedirs(PERSIST_DIRECTORY)
        vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=self.embeddings)
        print("Vectorstore created and connected to Chroma")
        return vectorstore

class DocumentHandler:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def ensure_upload_directory(self):
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)

    def load_pdf(self, file_path):
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    print("load pdf print text",page_text)
                    if page_text:
                        text += page_text + "\n"
                print(f"Extracted text from PDF: {text[:500]}...")  # Print first 500 characters of extracted text
                return text
        except Exception as e:
            print(f"Error loading PDF {file_path}: {e}")
            return ""

    def load_html(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text(separator="\n")
            print(f"Extracted text from HTML: {text[:500]}...")
            return text
        except Exception as e:
            print(f"Error loading HTML {file_path}: {e}")
            return ""

    def load_md(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = markdown.markdown(f.read())
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text(separator="\n")
            print(f"Extracted text from Markdown: {text[:500]}...")
            return text
        except Exception as e:
            print(f"Error loading Markdown {file_path}: {e}")
            return ""

    def load_txt(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"Extracted text from TXT: {text[:500]}...")
            return text
        except Exception as e:
            print(f"Error loading TXT {file_path}: {e}")
            return ""

    def load_docx(self, file_path):
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            print(f"Extracted text from DOCX: {text[:500]}...")
            return text
        except Exception as e:
            print(f"Error loading DOCX {file_path}: {e}")
            return ""

    def process_and_store_documents(self, files):
        all_texts = []
        self.ensure_upload_directory()  # Ensure the upload directory exists

        for file in files:
            # Save the file to the upload directory
            file_path = os.path.join(UPLOAD_DIRECTORY, secure_filename(file.filename))
            file.save(file_path)
            print(f"Saved file to {file_path}")

            # Extract text based on file type
            content = ""
            if file.filename.endswith('.pdf'):
                content = self.load_pdf(file_path)
            elif file.filename.endswith('.html'):
                content = self.load_html(file_path)
            elif file.filename.endswith('.md'):
                content = self.load_md(file_path)
            elif file.filename.endswith('.txt'):
                content = self.load_txt(file_path)
            elif file.filename.endswith('.docx'):
                content = self.load_docx(file_path)
            else:
                print(f"Unsupported file format: {file.filename}")
                continue

            if content.strip():
                print(f"Processing document: {file.filename}, Content length: {len(content)}")
                chunks = self.text_splitter.split_text(content)
                all_texts.extend(chunks)
            else:
                print(f"No content extracted from {file.filename}")

        if all_texts:
            try:
                print(f"Storing {len(all_texts)} chunks in vectorstore")
                self.vectorstore.add_texts(texts=all_texts)
                print("Embeddings stored successfully")
            except Exception as e:
                print(f"Error storing embeddings: {e}")
        else:
            print("No valid text chunks to store")

        return self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})



class QuestionAnswering:
    def __init__(self, model, prompt_template):
        self.model = model
        self.prompt_template = prompt_template

    def generate_response(self, context, question):
        chain_input = {"context": context, "question": question}
        response = self.prompt_template.format(**chain_input)
        return self.model.invoke(response)
