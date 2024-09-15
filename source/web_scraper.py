import time
import requests

class reddit_scraper:

    def __init__(self, subreddit, filter: bool) -> None:
        self.base_url = "https://www.reddit.com"
        self.subreddit = f"/r/{subreddit}" #subreddit name you want to pull from
        self.category = '/hot'
        #params for get request
        self.params = {'limit':100,'t': 'week', 'after': None}

        self.url = f"{self.base_url}{self.subreddit}{self.category}.json"
        self.filter: bool = filter

    def scrape_data(self) -> list[dict[str,str]]:
        response = requests.get(self.url,params=self.params)
        top_results = response.json()['data']['children']
        formatted_results = []

        for index,item in enumerate(top_results):
            if index==0:
                continue
            
            description = item['data']['selftext']
            title = item['data']['title']
            if filter:
                if description.count(" ") <= 200:
                    formatted_results.append({'title' : title, 'description' : description})

                else:
                    continue

            else:
                formatted_results.append({'title' : title, 'description' : description})

        return formatted_results


