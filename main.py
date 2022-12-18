import os
import time
import tweepy
import requests
import shutil
import random


api_key = 'api_key'
api_secret = 'api_secret'
bearer_token = r'bearer_token'
access_token = 'access_token'
access_token_secret = 'access_token_secret'

# Authentication of consumer key and secret
auth = tweepy.OAuthHandler(api_key, api_secret)

# Authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token, api_key, api_secret, access_token,access_token_secret)


#Check if tweet has already been posted
def check_tweet_exists(title):
  tweets = api.user_timeline(count=100)
  for tweet in tweets:
    if title in tweet.text:
      return True
  return False


# Tweet function
def tweetingTheTweets():
  #name of the subreddit you want
  subReddit = [
    "rareinsults", "cursedcomments", "HolUp", "meme", "memes",
    "PornhubComments", "wholesomememes", "shitposting", "funny",
    "Memes_Of_The_Dank", "dankmemes", "ComedyCemetery", "Animemes",
    "MemeEconomy", "terriblefacebookmemes"
  ]
  theChosenOne = random.choice(subReddit)
  print("**" + theChosenOne + "**")

  # Meme API
  response = requests.get("https://meme-api.com/gimme/" + theChosenOne)
  m = response.json()
  title = (m["title"])
  url = (m["url"])
  postLink = (m["postLink"])
  finalPostLink = postLink.translate({('https://'): None})
  print(title)
  print(url)
  print(m["ups"])

  if m["ups"] >= 500 and not check_tweet_exists(title):
    # Download the image
    file_name = "meme.jpg"
    res = requests.get(url, stream=True)
    if res.status_code == 200:
      with open(file_name, 'wb') as f:
        shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', file_name)
    else:
      print('Image Couldn\'t be retrieved')

    try:
      what_to_tweet = title + "  " + finalPostLink + " \n #memes #meme #funny " + "#" + theChosenOne
      media = api.media_upload("meme.jpg")
      api.update_status(what_to_tweet, media_ids=[media.media_id_string])
      print('Tweet posted successfully!')
      print('************************************************************')

    except Exception as error:
      print(error)
      print('************************************************************')

  else:
    print("Skipping this meme")
    print('************************************************************')


def main():
  while True:
    tweetingTheTweets()
    time.sleep(20)


if __name__ == "__main__":
  main()
