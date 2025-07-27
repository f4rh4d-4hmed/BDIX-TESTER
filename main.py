import requests
import colorama
from colorama import Fore, Style, init
import re
import webbrowser
import random
import time

init(convert=True)

import os
import sys

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file if line.strip()]
    return links

def check_link(link):
    try:
        if not link.startswith('http://') and not link.startswith('https://'):
            link = 'http://' + link
        start_time = time.time()
        response = requests.get(link, timeout=2) ##Increase timeout to catch more IP.
        latency = int((time.time() - start_time) * 1000)
        if response.status_code == 200:
            return f"{Fore.GREEN}Working{Style.RESET_ALL} - {latency}ms"
        elif response.status_code == 301 or response.status_code == 302:
            return f"{Fore.YELLOW}May contain threat{Style.RESET_ALL}" 
        else:
            return f"{Fore.RED}Not working{Style.RESET_ALL}"
    except requests.exceptions.RequestException:
        return f"{Fore.RED}Not working{Style.RESET_ALL}"

def strip_color_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def save_working_links(links, output_file):
    with open(output_file, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def process_links(links):
    working_links = []
    for i, link in enumerate(links, start=1):
        status = check_link(link)
        number_color = Fore.WHITE
        link_color = Fore.LIGHTBLUE_EX
        status_color = Fore.GREEN if "Working" in status else (Fore.RED if "Not working" in status else Fore.YELLOW)
        latency_color = Fore.LIGHTBLUE_EX
        
        if "Working" in status:
            status_split = status.split(" - ")
            print(f"{number_color}{i}. {Style.RESET_ALL}{link_color}{link}{Style.RESET_ALL} - {status_color}{status_split[0]}{Style.RESET_ALL} - {latency_color}{status_split[1]}{Style.RESET_ALL}")
            working_links.append(link)
        else:
            print(f"{number_color}{i}. {Style.RESET_ALL}{link_color}{link}{Style.RESET_ALL} - {status_color}{status}{Style.RESET_ALL}")
    return working_links

def open_links_in_browser(links, selected_indices):
    index_ranges = []
    for index_range in selected_indices.split(','):
        if '-' in index_range:
            start, end = map(int, index_range.split('-'))
            index_ranges.extend(range(start, end + 1))
        else:
            index_ranges.append(int(index_range))

    for index in sorted(set(index_ranges)):
        if 1 <= index <= len(links):
            webbrowser.open(links[index - 1])
        else:
            print(f"Invalid index: {index}")

try:
    links = read_links_from_file(resource_path('url.txt'))

    colors = [Fore.RED, Fore.GREEN, Fore.BLUE]
    greeting = r"""
 ____   ____   ___ __  __        _____             _               
| __ ) |  _ \ |_ _|\ \/ /       |_   _|  ___  ___ | |_   ___  _ __ 
|  _ \ | | | | | |  \  /  _____   | |   / _ \/ __|| __| / _ \| '__|
| |_) || |_| | | |  /  \ |_____|  | |  |  __/\__ \| |_ |  __/| |   
|____/ |____/ |___|/_/\_\         |_|   \___||___/ \__| \___||_|   
                                                                   
"""
    colored_greeting = ''.join(random.choice(colors) + char for char in greeting)
    print(colored_greeting, end='')

    additional_links = input("\nIf you want to scan more links, paste them here. Otherwise, leave it blank: ")
    if additional_links:
        additional_links = additional_links.split()
        links.extend(additional_links)

    working_links = process_links(links)

    save_working_links(working_links, resource_path('works.txt'))

    print("\n\nWhat do you want to do?\n\n1. Open all links in browser (Only Working)\n\n2. Only open the links I want\n")

    while True:
        user_choice = input("Enter your choice (1 or 2): ").strip()
        if user_choice in ['1', '2']:
            break
        else:
            print("Invalid choice. Please enter either 1 or 2.")

    if user_choice == '1':
        for link in working_links:
            webbrowser.open(link)
    elif user_choice == '2':
        selected_indices = input("Select/choose links by giving corresponding number(s): ").strip()
        open_links_in_browser(working_links, selected_indices)

    colors = [Fore.RED, Fore.GREEN, Fore.BLUE]
    author = "This code was developed by Farhad Ahmed\nFor more information visit me at http://github.com/f4rh4d-4hmed"

    colored_text = ''.join(random.choice(colors) + char for char in author)
    print(colored_text)

except KeyboardInterrupt:
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nExiting:)")
except FileNotFoundError:
    print(f"Error: Could not find 'url.txt' file. Please make sure it exists in the same directory as the script.")
except Exception as e:
    print(f"An error occurred: {e}")
