from colorama import Fore, Style

def print_intro(s):
    print(Fore.RED + s)

def print_options(tickers, num_posts):
    print(Fore.MAGENTA + "Tickers:\t", tickers)
    print(Fore.MAGENTA + "#Posts: \t", num_posts)
    print()

def print_link(s):
    print(f'[{Fore.YELLOW}{s}{Style.RESET_ALL}]')

def print_tickers(tickers):
    for ticker in tickers:
        print(Fore.BLUE + ticker, end=" ")

    print()