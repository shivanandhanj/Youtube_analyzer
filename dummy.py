from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline, AutoTokenizer

# Initialize pipelines for question-answering and summarization
qa_model = pipeline('question-answering')
summarizer = pipeline('summarization', model="sshleifer/distilbart-cnn-12-6")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    import re
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

def get_transcript(video_id):
    """
    Fetches the transcript of a YouTube video using the video ID.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"An error occurred while fetching transcript: {e}")
        return None

def format_transcript_for_summarizer(transcript):
    """
    Concatenates the transcript texts into a single string for summarization.
    """
    return ' '.join([entry['text'] for entry in transcript])

def split_text_into_chunks(text, max_tokens=1024):
    """
    Splits the text into chunks of the specified token length using the tokenizer.
    """
    words = text.split()
    current_chunk = []
    current_length = 0
    chunks = []

    for word in words:
        # Encode the word and get the number of tokens
        word_tokens = tokenizer.encode(word, add_special_tokens=False)
        word_token_length = len(word_tokens)

        # If adding this word exceeds the max length, save the current chunk
        if current_length + word_token_length > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_token_length
        else:
            current_chunk.append(word)
            current_length += word_token_length

    # Add any remaining words as the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def summarize_text(text):
    """
    Summarizes the given text by breaking it into manageable chunks.
    """
    summaries = []
    
    # Split text into chunks of 1024 tokens
    chunks = split_text_into_chunks(text)
    
    # Summarize each chunk
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    return ' '.join(summaries)

def ask_question(transcript, question):
    """
    Uses the question-answering model to answer a question based on the video transcript.
    """
    context = ' '.join([t['text'] for t in transcript])
    answer = qa_model(question=question, context=context)
    return answer['answer']

# Example usage
video_url = 'https://www.youtube.com/watch?v=6h9sjYm9vTE'

# Extract the video ID from the URL
video_id = extract_video_id(video_url)

if video_id:
    # Fetch the transcript
    transcript = get_transcript(video_id)
    text_values = [d["text"] for d in transcript if "text" in d]
    print(text_values)

    if transcript:
        # Format transcript for summarization
        formatted_transcript = format_transcript_for_summarizer(transcript)
        
        # Summarize the transcript
        summary = summarize_text(formatted_transcript)
        print("Summary of the video:")
        print(summary)

        # Ask a question about the video content
        question = "What is the video about?"
        answer = ask_question(transcript, question)
        print(f"Answer to '{question}': {answer}")
else:
    print("Invalid video URL or video ID could not be extracted.")
