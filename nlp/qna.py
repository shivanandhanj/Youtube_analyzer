import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Clean the transcript to remove newline characters or other unwanted characters
def clean_transcript(text):
    return re.sub(r'\s+', ' ', text).strip()

# Retrieve relevant passages from the transcript
def retrieve_relevant_passages(transcript, question):
    # Split transcript into sentences or chunks for better processing
    documents = [transcript[i:i+1024] for i in range(0, len(transcript), 1024)]
    
    # Handle the edge case where there are no documents
    if not documents:
        return ""
    
    vectorizer = TfidfVectorizer().fit_transform(documents + [question])
    
    # Compute similarity between the question and each document
    similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1])
    
    # Get the top N most relevant passages, handle cases with fewer than 3 passages
    num_passages = min(3, len(documents))
    top_n_indices = similarities.argsort()[0][-num_passages:][::-1]
    relevant_passages = [documents[i] for i in top_n_indices]
    
    return ' '.join(relevant_passages)

# QA model using Hugging Face's pipeline for question-answering
qa_model = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')

def generate_answer(retrieved_passages, question):
    if not retrieved_passages:
        return "No relevant information found."

    # Use the QA model to generate the answer
    answer = qa_model(question=question, context=retrieved_passages)
    return answer['answer']

# Main function to ask a question and get an answer
def ask_question(transcript, question):
    # Clean the transcript and prepare it
    cleaned_transcript = clean_transcript(transcript)
    
    # Retrieve the most relevant parts of the transcript
    retrieved_passages = retrieve_relevant_passages(cleaned_transcript, question)
    
    # Generate the answer based on retrieved passages and question
    answer = generate_answer(retrieved_passages, question)
    
    return answer
