import os
import requests
import json
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import redis


load_dotenv()

CONSUMER_KEY = os.getenv("TWITTER_API_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
API_KEY = os.getenv("WAKATIME_API_KEY")

r = redis.Redis(host="localhost", port=6379, db=0)


auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def get_wakatime_stats():
    waka_url = (
        f"https://wakatime.com/api/v1/users/current/status_bar/today?api_key={API_KEY}"
    )
    response = requests.get(waka_url)
    if response.status_code != 200:
        raise Exception(
            f"Request failed with error {response.status_code}, {response.text}"
        )

    stats = {}
    top_3_languages = {}
    stats["minutes_coded_today"] = response.json()["data"]["grand_total"]["text"]

    for language in response.json()["data"]["languages"][0:3]:
        top_3_languages[language["name"]] = language["text"]
    return stats, top_3_languages


# def update_coding_streak():
#     with open("coding_streak.txt", "r") as f:
#         coding_streak = int(f.read().strip())

#     stats, top_3_languages = get_wakatime_stats()
#     if stats["minutes_coded_today"]:
#         coding_streak += 1
#     else:
#         coding_streak = 0

#     with open("coding_streak.txt", "w") as f:
#         f.write(str(coding_streak))

#     # If the coding streak is broken, do not tweet and end the program.  The streak file will be updated to 0.
#     if coding_streak == 0:
#         print("Coding streak broken, not tweeting")
#         exit()

#     return coding_streak


def update_coding_streak():
    # get the current streak from redis
    coding_streak = r.get("coding_streak")
    # if there is no streak, set it to 1 and save it to redis
    if not coding_streak:
        coding_streak = 1
        r.set("coding_streak", coding_streak)
    # if there is a streak, increment it and save it to redis
    else:
        coding_streak = int(coding_streak) + 1
        r.set("coding_streak", coding_streak)

    return coding_streak


def format_tweet(coding_streak, minutes_coded_today, languages):
    day_of_streak = coding_streak
    tweet_text = f"Day {day_of_streak} of my coding streak: I coded {minutes_coded_today} today!\n\n#100DaysOfCode "
    # make the hashtags each language
    for language in languages.keys():
        tweet_text += f"#{language} "

    return tweet_text


def post_tweet(tweet_text):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    data = {"text": tweet_text}
    response = requests.post(url, auth=auth, data=json.dumps(data), headers=headers)

    if response.status_code != 201:
        raise Exception(
            f"Request failed with error {response.status_code}, {response.text}"
        )

    print("Tweet posted successfully!", response.json())


if __name__ == "__main__":
    stats, languages = get_wakatime_stats()
    if stats["minutes_coded_today"]:
        coding_streak = update_coding_streak()
    else:
        exit()

    tweet_text = format_tweet(coding_streak, stats["minutes_coded_today"], languages)
    post_tweet(tweet_text)
