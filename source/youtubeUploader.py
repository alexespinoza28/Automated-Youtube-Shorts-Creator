from youtube_uploader_selenium import YouTubeUploader
import json

class Uploader:
    def upload(self, description, title, video_path, post_data, thumbnail_path):
        video_path = '123/rockets.flv'
       

        post_data = {
        "title": title,
        "description": description,
        "tags": ["reddit", "redditstories", "shorts"],
        "schedule": "06/05/2013, 23:05"
        }

    
        uploader = YouTubeUploader(video_path, post_data, thumbnail_path)
        was_video_uploaded, video_id = uploader.upload()
        assert was_video_uploaded

        