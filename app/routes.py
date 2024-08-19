from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from app.models import LLMModel, DocumentHandler, QuestionAnswering
import uuid

# In-memory store for retrievers
retriever_store = {}

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_files():
        if request.method == 'POST':
            files = request.files.getlist('files')
            print("files from upload",files)
            try:
                model_instance = LLMModel()
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('index'))

            vectorstore = model_instance.create_vector_store()
            document_handler = DocumentHandler(vectorstore)
            retriever = document_handler.process_and_store_documents(files)

            retriever_key = str(uuid.uuid4())  # Generate a unique key
            retriever_store[retriever_key] = retriever  # Store retriever in the in-memory store

            session['retriever_key'] = retriever_key  # Store the key in the session
            flash('Documents uploaded and processed successfully!', 'success')
            return redirect(url_for('ask_question'))
        return render_template('upload.html')

    @app.route('/ask', methods=['GET', 'POST'])
    def ask_question():
        if 'conversation' not in session:
            session['conversation'] = []

        if request.method == 'POST':
            try:
                question = request.form['question']
                retriever_key = session.get('retriever_key')
                retriever = retriever_store.get(retriever_key)

                if not retriever:
                    flash("Retriever not found.", 'error')
                    return redirect(url_for('index'))

                model_instance = LLMModel()
                prompt_template = """
                    Answer the question based on the context below. If you can't 
                    answer the question, reply "I don't know".

                    Context: {context}

                    Question: {question}
                """

                qa_instance = QuestionAnswering(model_instance.model, prompt_template)
                print(f"Asking question: {question}")
                
                # Use the invoke method for retrieval
                retriever_results = retriever.invoke({"query": question})
                print(f"Retriever results: {retriever_results}")

                if retriever_results:
                    context = " ".join([doc.page_content for doc in retriever_results])
                    print(f"Context for model: {context[:500]}...")  # Print first 500 chars of context
                else:
                    context = ""
                    print("No relevant documents found")

                response = qa_instance.generate_response(context, question)
                print(f"Generated response: {response}")

                session['conversation'].append({"question": question, "response": response})
                return redirect(url_for('ask_question'))
            except Exception as e:
                print(f"Error: {str(e)}")
                flash(f"An error occurred: {str(e)}", 'error')
                return redirect(url_for('ask_question'))

        return render_template('ask.html', conversation=session['conversation'])
