import os
import requests
import json
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv("TWITTER_API_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
API_KEY = os.getenv("WAKATIME_API_KEY")


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
    stats["minutes_coded_today"] = response.json()["data"]["grand_total"]["text"]
    stats["total_seconds_coded_today"] = response.json()["data"]["grand_total"][
        "total_seconds"
    ]
    return stats


def update_coding_streak():
    with open("coding_streak.txt", "r") as f:
        coding_streak = int(f.read().strip())

    stats = get_wakatime_stats()
    if stats["total_seconds_coded_today"] > 0:
        coding_streak += 1
    else:
        coding_streak = 0

    with open("coding_streak.txt", "w") as f:
        f.write(str(coding_streak))

    # If the streak is 0, we don't want to tweet about it so we will end the program
    if coding_streak == 0:
        print("No coding today, so no tweet!")
        exit()

    return coding_streak


def format_tweet(coding_streak, minutes_coded_today):
    day_of_streak = coding_streak
    tweet_text = f"Day {day_of_streak} of my coding streak: I coded {minutes_coded_today} minutes today!\n\n#100DaysOfCode #100DaysOfDjango #python #django"
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
    coding_streak = update_coding_streak()
    stats = get_wakatime_stats()
    tweet_text = format_tweet(coding_streak, stats["minutes_coded_today"])
    post_tweet(tweet_text)
