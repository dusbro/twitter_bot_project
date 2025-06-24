import tweepy
import os
import requests
import feedparser
from dotenv import load_dotenv

def get_client():
    load_dotenv()

    # Twitter API keys from .env file
    client = tweepy.Client(
        consumer_key = os.getenv("CONSUMER_KEY"),
        consumer_secret = os.getenv("CONSUMER_SECRET"),
        access_token = os.getenv("ACCESS_TOKEN"),
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET"),
        bearer_token= os.getenv("BEARER_TOKEN"),
        wait_on_rate_limit=True
    )

    return client

# RSS Feed for fetching latest news
def fetch_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    if feed.entries:
        return feed.entries[0].title + " - " + feed.entries[0].link
    return None

# Function to generate a twet using Ollama
def generate_tweet(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False #Ensures response is not streamed
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("response","").strip()
    return "Error: Could not generate tweet."

# Function to create and post a tweet    
def create_tweet(client, tweet_text):
    client.create_tweet(text=tweet_text)

# Initialize Twitter clinet
client = get_client()

# Define RSS feed URL (Can change to desired news source)
feed_url = "https://aiacceleratorinstitute.com/rss/"

# Define the tweet topic
news_summary = fetch_rss_feed(feed_url)
tweet_prompt = f"Write a tweet about this news: {news_summary}, only include the tweet message, and do not put the message in quotes" if news_summary else "Write a tweet about the latest AI Trends,only include the tweet message, and do not put the message in quotes"

# Generate tweet using Ollama
tweet_text = generate_tweet(tweet_prompt)

# Post tweet
create_tweet(client, tweet_text)

print("Tweet posted:", tweet_text)


