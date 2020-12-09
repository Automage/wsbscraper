import sys
import os
import argparse
import json
import praw
from dotenv import load_dotenv


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


# Env Setup

SECRET, ID, USER_AGENT = setup_env()
parser = setup_args()
print("SECRET=%s ID=%s USER_AGENT=%s" % (SECRET, ID, USER_AGENT))

# PRAW Setup

reddit = praw.Reddit(client_id=ID, client_secret=SECRET, user_agent=USER_AGENT)

# Parse arguments

options = parser.parse_args(sys.argv[1:])
num_posts = options.numposts
tickers = options.tickers
