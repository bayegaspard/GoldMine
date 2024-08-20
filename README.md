# VectorShield

### DEFCON32 TALK
**Leverage Gen-AI+RAG to stay ahead in the cyber battle! Building Your Red-Teaming Co-Pilot.**

VectorShield is a proof-of-concept (PoC) application from my DEFCON32 talk, designed to enhance red-teaming operations by leveraging Generative AI combined with Retrieval-Augmented Generation (RAG). This early version supports various document types and is under constant development. Contributions are welcome!

## Features

- **Multi-Document Support**: Upload and process multiple file types, including PDFs, HTML, Markdown, and plain text.
- **Generative AI Integration**: Powered by the Ollama model to generate intelligent responses based on your document corpus.
- **RAG (Retrieval-Augmented Generation)**: Combines document retrieval with generative AI to provide contextually relevant answers.
- **User-Friendly Interface**: Simple web interface to upload documents and ask questions.

## Supported File Types

- **PDF** (.pdf)
- **HTML** (.html)
- **Markdown** (.md)
- **Plain Text** (.txt)

## Requirements

- **Python 3.10+**
- **Ollama**: Generative AI model used for generating answers.
- **LangChain**: For handling RAG (Retrieval-Augmented Generation) processes.
- **Flask**: Web framework to serve the application.
- **Various Python Packages**: Specified in `requirements.txt`.
- **Chroma requires SQLite > 3.35**, if you encounter issues with having too low of a SQLite version please try following steps to fix it using this [link](https://docs.trychroma.com/troubleshooting#sqlite)

## Installation and Setup

Follow these steps to set up the VectorShield application:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/vectorshield.git
   cd vectorshield
   ```
2. **Set Up a Virtual Environment:**
  ```bash
  conda create -n venv python=3.10 anaconda~
  ```

Activate the Virtual Environment:
- On Windows: `conda activate venv`
- On macOS/Linux: `conda activate venv`

If you don't have conda installed, you can follow this [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) on how to install conda.

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```
4. **Run the Application:**
python run.py

### Contribution
This is an early version of VectorShield, and it's under continuous development. Contributions, feedback, and ideas are highly encouraged! Whether you're fixing bugs, adding features, or improving documentation, your input is valuable.

### License
This project is licensed under the terms specified in the [LICENSE](https://github.com/bayegaspard/VectorShield/blob/main/LICENSE)
 file.


