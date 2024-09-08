from transformers import pipeline, AutoTokenizer

# Initialize summarization pipeline and tokenizer
summarizer = pipeline('summarization', model="sshleifer/distilbart-cnn-12-6")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

def split_text_into_chunks(text, max_tokens=1024):
    """
    Splits the text into chunks of the specified token length using the tokenizer.
    """
    words = text.split()
    current_chunk = []
    current_length = 0
    chunks = []

    for word in words:
        word_tokens = tokenizer.encode(word, add_special_tokens=False)
        word_token_length = len(word_tokens)

        if current_length + word_token_length > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_token_length
        else:
            current_chunk.append(word)
            current_length += word_token_length

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
