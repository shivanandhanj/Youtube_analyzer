import re

def extract_video_id(url):
    video_id = re.search(r"(?<=v=)[^&#]+", url)
    if not video_id:
        video_id = re.search(r"(?<=be/)[^&#]+", url)
    return video_id.group(0) if video_id else None
