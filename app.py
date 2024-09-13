from flask import Flask, render_template, request, jsonify
from utils.youtube import extract_video_id, get_transcript
from nlp.summarization import summarize_text
from nlp.qna import ask_question
from youtube_api.youtube_client import get_video_details, get_video_comments, get_most_liked_comments, get_comments_with_timestamps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    
    data = request.get_json()
    video_url = data.get('video_url')
    print(video_url)
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
        answer = ask_question(formatted_transcript, question)

    return jsonify({
        'transcript': formatted_transcript,
        'summary': summary,
        'answer': answer
    })


@app.route('/comment-details',methods=['POST'])
def get_comments():
    data = request.get_json()
    video_url = data.get('video_url')
   
    video_id=extract_video_id(video_url)
    if video_id:
        # Fetch video details
        
        comments=get_video_comments(video_id)
       
        cmt_likes=get_most_liked_comments(video_id)
      
        cmt=get_comments_with_timestamps(video_id)
        

     
    return jsonify({
        'all_comments':comments,
        'top_comments':cmt_likes,
        'timestamped_comments':cmt
    })
        
   


@app.route('/details',methods=['POST'])
def get_details():
    data = request.get_json()
    video_url = data.get('video_url')
   
    video_id=extract_video_id(video_url)

    if video_id:
        # Fetch video details
        details = get_video_details(video_id)
        get_video_comments(video_id)
        cmt=[]
        cmt=get_most_liked_comments(video_id)
        print(cmt)
        cmt=get_comments_with_timestamps(video_id)
        print(cmt)

        if details:
            return jsonify(details)
        else:
            return jsonify({'error': 'Video not found'}), 404
    else:
        return jsonify({'error': 'Invalid video URL'}), 400


if __name__ == '__main__':
    app.run(debug=True)
