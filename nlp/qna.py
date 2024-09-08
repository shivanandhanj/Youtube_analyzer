from transformers import pipeline

# Initialize question-answering pipeline
qa_model = pipeline('question-answering')

def ask_question(transcript, question):
    """
    Uses the question-answering model to answer a question based on the video transcript.
    """
    context = ' '.join([t['text'] for t in transcript])
    answer = qa_model(question=question, context=context)
    return answer['answer']
