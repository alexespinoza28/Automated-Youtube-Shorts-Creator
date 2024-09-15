import re
from web_scraper import reddit_scraper
from moviepytest import Editor
from transcriber import VideoTranscriber

# Grabs a list of the top 100 posts, filters the list to only include entries with 200 words or under
#top_posts_tifu = reddit_scraper("TIFU",True).scrape_data()
top_posts_aitah = reddit_scraper("AITAH", True).scrape_data()

count = 0
for post in top_posts_aitah:
    if count == 1:
        exit()
    title = post["title"]
    description = post["description"]
    
    
    # Create the video (be cautious about the cost)
    output_file ='bruhaita' + str(count) + '.mp4'

    #Editor().createVids(title, description, output_file)
    
    # Add captions to the video
    addCaptions = VideoTranscriber()
    output_path = addCaptions.transcribe(output_file , 'captions' + output_file )
    count += 1

# This line costs money, be careful
# Editor().createVids(top_posts_tifu[0]["title"], top_posts_tifu[0]["description"], 'preCaption/' + top_posts_tifu[0]["title"] + '.mp4')

# THIS ADDs captions
# addCaptions = VideoTranscriber()
# output_path = addCaptions.transcribe('source/preCaption/' + top_posts_tifu[0]["title"] + '.mp4', 'source/finishedVids/' + top_posts_tifu[0]["title"] + '.mp4')

# upload vid
# Uploader(top_posts_tifu[0]["title"], top_posts_tifu[0]["title"], output_path, post_data, thumbnail_path)
