import sys
import os
import argparse
import praw
from colorama import init
from dotenv import load_dotenv
from util import print_intro, print_options, print_comment, print_post

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


def setup():
    # Init colorama to reset after every print
    init(autoreset=True) 

    # Env Setup
    SECRET, ID, USER_AGENT = setup_env()
    # print("SECRET=%s ID=%s USER_AGENT=%s" % (SECRET, ID, USER_AGENT))

    # Setup parser and arguments
    parser = setup_args()

    # PRAW Setup
    reddit = praw.Reddit(client_id=ID, client_secret=SECRET, user_agent=USER_AGENT)

    return parser, reddit


class WSBScraper:
    def __init__(self, reddit, tickers, num_posts):
        self.reddit = reddit
        self.tickers = tickers
        self.num_posts = num_posts


    # Search comment for tickers and print matches
    def ticker_search(self, comment):
        matches = {x for x in self.tickers if x in comment.body}
        if len(matches) != 0:
            print_comment(comment, list(matches))

    # Scrape top comments from hot posts and print ticker matches
    def scrape(self):
        # Get top n posts
        posts = self.reddit.subreddit('wallstreetbets').hot(limit=(self.num_posts + 1))
        posts = [post for post in posts]

        # Skip daily discussion
        posts = posts[1:]

        # Search each post for tickers in top comments
        j = 1
        for post in posts:
            print_post(post, j)
            submission = self.reddit.submission(id=post.id)
            submission.comment_sort = 'top'
            submission.comments.replace_more(limit=0)
            i = 0
            for comment in submission.comments.list():
                self.ticker_search(comment)
                # Limit search to top 30 comments per post
                i = i + 1
                if i > 50:
                    break

            j = j + 1


def main():
    # Obnoxious title message
    print_intro(INTRO_MSG)

    # Read .env, setup PRAW, get arguments
    parser, reddit = setup()

    # Parse arguments
    options = parser.parse_args(sys.argv[1:])
    num_posts = options.numposts
    tickers = options.tickers

    # Print options 
    print_options(tickers, num_posts)

    # Begin scraping
    scraper = WSBScraper(reddit, tickers, num_posts)
    scraper.scrape()


if __name__ == "__main__":
    main()