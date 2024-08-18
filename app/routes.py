from flask import render_template, request, redirect, url_for, flash, session
from app import create_app
from app.models import LLMModel, DocumentHandler, QuestionAnswering

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('files')
        model_instance = LLMModel()
        vectorstore = model_instance.create_vector_store()

        document_handler = DocumentHandler(vectorstore)
        retriever = document_handler.process_and_store_documents(files)

        session['retriever'] = retriever
        flash('Documents uploaded successfully!', 'success')
        return redirect(url_for('ask_question'))
    return render_template('upload.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        try:
            question = request.form['question']
            retriever = session.get('retriever')
            model_instance = LLMModel()
            prompt_template = PromptTemplate.from_template("""
                Answer the question based on the context below. If you can't 
                answer the question, reply "I don't know".

                Context: {context}

                Question: {question}
            """)

            qa_instance = QuestionAnswering(model_instance.model, prompt_template)
            retriever_results = retriever.invoke(question)
            context = " ".join([doc.page_content for doc in retriever_results])

            response = qa_instance.generate_response(context, question)
            session['conversation'].append({"question": question, "response": response})
            return redirect(url_for('ask_question'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('ask_question'))

    return render_template('ask.html', conversation=session['conversation'])
