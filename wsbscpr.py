import sys
import os
import argparse
import json

import config

# Set arguments

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--numposts', type=int,
                    required=True, help='Number of posts to scan')
parser.add_argument('-t', '--tickers', nargs='+',
                    required=True, help='Tickers to look for')


# Parse arguments

options = parser.parse_args(sys.argv[1:])
num_posts = options.numposts
tickers = options.tickers
