# GoldMine

### DEFCON32 TALK
**Leverage Gen-AI+RAG to stay ahead in the cyber battle! Building Your Red-Teaming Co-Pilot.**

GoldMine is a proof-of-concept (PoC) application from my DEFCON32 talk. It is designed to enhance red-teaming operations by leveraging Generative AI combined with Retrieval-Augmented Generation (RAG). This early version supports various document types and is under constant development. Contributions are welcome!

## Features

- **Multi-Document Support**: Upload and process multiple file types, including PDFs, Docx, HTML, Markdown, and plain text.
- **Generative AI Integration**: Powered by the Ollama model to generate intelligent responses based on your document corpus.
- **RAG (Retrieval-Augmented Generation)** combines document retrieval with generative AI to provide contextually relevant answers.
- **User-Friendly Interface**: Simple web interface to upload documents and ask questions.

## Supported File Types

- **PDF** (.pdf)
- **HTML** (.html)
- **Markdown** (.md)
- **Docx** (.docx)
- **Plain Text** (.txt)

## Requirements

- **Python 3.10+**
- **Ollama**: Framework used to run the generative AI. In this project, we use llama3. If you don't have Ollama installed, you can use this [link](https://ollama.com/download) to install Ollama on Windows and Linux.
- **LangChain**: This handles RAG (Retrieval-Augmented Generation) processes.
- **Flask**: Web framework to serve the application.
- **Various Python Packages**: Specified in `requirements.txt`.
- **Chroma requires SQLite > 3.35**, if you encounter issues with having too low of a SQLite version, please try following steps to fix it using this [link](https://docs.trychroma.com/troubleshooting#sqlite)

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
```bash
python run.py
```

#### Proof of Concept (PoC) - May contain bugs
![POC]([URL_or_path_to_image](https://github.com/bayegaspard/GoldMine/blob/main/poc-pics/poc.png))

**Disclaimer:**  
This project is under development, a Proof of Concept (PoC), and has not been thoroughly tested for production-level deployment. While it showcases the idea's core functionality and potential, it may contain bugs, lack full feature coverage, and still need to meet the robustness required for production environments.

**Call for Contributors:**  
We believe in this project's potential, and with the community's support, we can refine and enhance it to reach production-level quality. Your contributions, whether through code, testing, documentation, or ideas, are highly valuable and appreciated. Together, we can evolve this project into a reliable, production-ready solution.

**How to Contribute:**
- Fork the repository and create a new branch for your contributions.
- Submit pull requests for bug fixes, features, or improvements.
- Participate in discussions and suggest enhancements.
- Could you share your testing results and help us identify areas for improvement?

Thank you for your interest and support in making this project a success!


### License
This project is licensed under the terms specified in the [LICENSE](https://github.com/bayegaspard/VectorShield/blob/main/LICENSE)
 file.


