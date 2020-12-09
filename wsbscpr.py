import sys
import os
import argparse
import json
import praw
from colorama import init, Fore
from dotenv import load_dotenv

# Doom font
INTRO_MSG = '''
 _    _ ___________  _____ _____ ______  ___  ______ ___________ 
| |  | /  ___| ___ \/  ___/  __ \| ___ \/ _ \ | ___ \  ___| ___ \\
| |  | \ `--.| |_/ /\ `--.| /  \/| |_/ / /_\ \| |_/ / |__ | |_/ /
| |/\| |`--. \ ___ \ `--. \ |    |    /|  _  ||  __/|  __||    / 
\  /\  /\__/ / |_/ //\__/ / \__/\| |\ \| | | || |   | |___| |\ \ 
 \/  \/\____/\____/ \____/ \____/\_| \_\_| |_/\_|   \____/\_| \_|
                                                                                                                       
'''

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--numposts', type=int,
                        required=True, help='Number of posts to scan')
    parser.add_argument('-t', '--tickers', nargs='+',
                        required=True, help='Tickers to look for')

    return parser


def setup_env():
    load_dotenv()
    return os.getenv('SECRET'), os.getenv('ID'), os.getenv('USER_AGENT')


def ticker_search(comment, tickers):
    print('Tickers: ', tickers)
    print(comment.body)
    print('[', comment.permalink, ']')
    print()

def main():
    print(Fore.RED + INTRO_MSG)

    # Env Setup
    init(autoreset=True) # Init colorama
    SECRET, ID, USER_AGENT = setup_env()
    parser = setup_args()
    # print("SECRET=%s ID=%s USER_AGENT=%s" % (SECRET, ID, USER_AGENT))
    # print()

    # PRAW Setup

    reddit = praw.Reddit(client_id=ID, client_secret=SECRET, user_agent=USER_AGENT)

    # Parse arguments

    options = parser.parse_args(sys.argv[1:])
    num_posts = options.numposts
    tickers = options.tickers

    print()
    print("Tickers:\t", tickers)
    print("#Posts: \t", num_posts)
    print()

    # Search posts

    posts = reddit.subreddit('wallstreetbets').hot(limit=(num_posts + 1))
    posts = [post for post in posts]

    # Skip daily discussion
    posts = posts[1:]

    for post in posts:
        print(post.title)
        print('[', post.url, ']')
        print()
        submission = reddit.submission(id=post.id)
        submission.comment_sort = 'top'
        submission.comments.replace_more(limit=0)
        i = 0
        for comment in submission.comments.list():
            ticker_search(comment, tickers)
            # Limit search to top 30 comments per post
            i = i + 1
            if i > 30:
                break


if __name__ == "__main__":
    main()