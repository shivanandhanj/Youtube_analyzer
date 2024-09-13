from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from config import API_KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_video_details(video_id):
    # Request video snippet and statistics (views, likes, etc.)
    request = youtube.videos().list(part="snippet,statistics", id=video_id)
    response = request.execute()
    
    # Extract the relevant details from the response
    if response['items']:
        video_data = response['items'][0]
        title = video_data['snippet']['title']
        description = video_data['snippet']['description']
        views = video_data['statistics'].get('viewCount', 'N/A')
        likes = video_data['statistics'].get('likeCount', 'N/A')
        comments = video_data['statistics'].get('commentCount', 'N/A')

        # Return a dictionary of video details
        return {
            'title': title,
            'description': description,
            'views': views,
            'likes': likes,
            'comments': comments
        }
    else:
        return None


def get_video_comments(video_id):
    # Make an API request to get comments
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=5  # Adjust as needed
    )
    
    response = request.execute()
    comment=[]
    # Extract and print comments
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    return comment

def get_most_liked_comments(video_id):
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=10,  # Adjust as needed
        order='relevance'  # You can use 'relevance' or 'time'
    )
    
    response = request.execute()

    # Extract comments and their like counts
    comments = []
    for item in response['items']:
        comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
        comments.append({'text': comment_text, 'likes': like_count})
    
    # Sort comments by likes in descending order
    comments_sorted_by_likes = sorted(comments, key=lambda x: x['likes'], reverse=True)

    return comments_sorted_by_likes

def get_comments_with_timestamps(video_id):
    # Request to get comments for the video
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100# Adjust as needed
    )
    
    response = request.execute()

    # Extract comments and look for timestamps
    comments_with_timestamps = []
    for item in response['items']:
        comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        if '0:' in comment_text or '1:' in comment_text:  # Check for simple timestamp patterns
            comments_with_timestamps.append(comment_text)
   
    return comments_with_timestamps


def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript
