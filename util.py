from colorama import Fore, Style

def print_title(s):
    print(Fore.MAGENTA + s)

def print_link(s):
    print(f'[{Fore.YELLOW}{s}{Style.RESET_ALL}]')

def print_tickers(tickers):
    for ticker in tickers:
        print(Fore.BLUE + ticker, end=" ")

    print()


# Exported

def print_intro(s):
    print(Fore.RED + s)

def print_options(tickers, num_posts):
    print(Fore.MAGENTA + "Tickers:\t", end=" ")
    print_tickers(tickers)
    print(Fore.MAGENTA + "#Posts: \t " + Fore.BLUE + str(num_posts))
    print()

def print_comment(comment, tickers):
    print(comment.body)
    print()
    print_tickers(tickers)
    print_link(comment.permalink)
    print()
    print(Fore.BLUE + "------")
    print()

def print_post(post, i):
    print()
    print(Fore.BLUE + "====== POST " + str(i))
    print()
    print_title(post.title)
    print_link(post.url)
    print()
    print(Fore.BLUE + "------")
    print()