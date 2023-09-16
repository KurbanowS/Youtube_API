import requests

from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'key' : current_app.config['YOUTUBE_API_KEY'],
        'q' : 'learn flask',
        'part' : 'snippet',
        'maxResults' : 9,
        'type' : 'video'
    }

    r = requests.get(search_url, params=search_params)

    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])
    
    video_params = {
        'key' : current_app.config['YOUTUBE_API_KEY'],
        'id' : ','.join(video_ids),
        'part' : 'snippet, contentDetails',
        'maxResults' : 9
    }

    r = requests.get(video_url, params=video_params)
    results = r.json()['items']

    videos = []
    for result in results:
        
        video_data = {
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            'duration' : result['contentDetails']['duration'],
            'title' : result['snippet']['title']
        }
        videos.append(video_data)


    return render_template('index.html', videos=videos)