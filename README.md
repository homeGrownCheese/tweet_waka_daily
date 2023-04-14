# Tweet Your Daily Coding Stats From WakaTime

## What is WakaTime?

[WakaTime](https://wakatime.com/) is a time tracking tool that automatically tracks how long you spend coding. It can track time spent in any text editor, IDE, terminal, browser, or operating system. It also has plugins for many popular programming languages and frameworks.

## What is this?
This is a script that will fetch your daily coding stats from WakaTime and Tweet them to your Twitter account.  This is a quick project meant to run on a local server with a cron job.

## How to use it?
1. Clone this repo
2. Create a Twitter app and get your API keys
3. Create a WakaTime account to get an API key
4. Create a `.env` file in the root directory and add the following:
```
TWITTER_CONSUMER_KEY=YOUR_CONSUMER_KEY
TWITTER_CONSUMER_SECRET=YOUR_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET=YOUR_ACCESS_TOKEN_SECRET
WAKATIME_API_KEY=YOUR_WAKATIME_API_KEY
```
5.  Set the `coding_stats.txt` file in the root directory to your current streak.  This file will be used to store the current day count you are on.  The first time you run the script, if this is the beginning of your streak this file should contain the number 1.  The next time you run the script, it should contain the number 2, and so on.  This process should be replaced with a database or redis in the future, but for now, this is a quick and dirty solution and easy to do for a local server.

6. Create a cron job to run the script every day at 12:00 AM or whatever time you want.  For example, to run the script every day at 12:00 AM, add the following to your crontab:
```
0 0 * * * /path/to/script
```
7. Enjoy your daily coding stats!  Free Twitter API limits are now 1500 tweets a month(although I'm having a hard time tracking down the actual usage), so you can run this script every day and not worry about hitting the limit.

