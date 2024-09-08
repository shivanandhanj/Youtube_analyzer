def format_transcript_for_summarizer(transcript):
    """
    Concatenates the transcript texts into a single string for summarization.
    """
    return ' '.join([entry['text'] for entry in transcript])
