from flask import Flask, render_template, request, jsonify
from utils.youtube import extract_video_id, get_transcript
from nlp.summarization import summarize_text
from nlp.qna import ask_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    data = request.get_json()
    video_url = data.get('video_url')
    question = data.get('question', '')

    # Extract video ID from URL
    video_id = extract_video_id(video_url)

    # Fetch transcript
    transcript = get_transcript(video_id)
    if not transcript:
        return jsonify({'error': 'Transcript could not be fetched.'}), 400

    # Format transcript for summarization
    formatted_transcript = ' '.join([entry['text'] for entry in transcript])

    # Summarize the transcript
    summary = summarize_text(formatted_transcript)

    # Answer question (if provided)
    answer = ''
    if question:
        answer = ask_question(transcript, question)

    return jsonify({
        'transcript': formatted_transcript,
        'summary': summary,
        'answer': answer
    })

if __name__ == '__main__':
    app.run(debug=True)
