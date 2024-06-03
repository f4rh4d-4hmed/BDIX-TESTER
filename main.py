import requests
import colorama
from colorama import Fore, Style, init
import re
import webbrowser
import random
import time
import keyboard

init(convert=True)

def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = file.read().splitlines()
    return links

def check_link(link):
    try:
        if not link.startswith('http://') and not link.startswith('https://'):
            link = 'http://' + link
        start_time = time.time()
        response = requests.get(link, timeout=3)
        latency = int((time.time() - start_time) * 1000)  # Calculating latency in milliseconds
        if response.status_code == 200:
            return f"{Fore.GREEN}Working{Style.RESET_ALL} - {latency}ms"
        elif response.status_code == 301 or response.status_code == 302:
            return f"{Fore.ORANGE}May contain threat{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}Not working{Style.RESET_ALL}"
    except requests.exceptions.RequestException:
        return f"{Fore.RED}Not working{Style.RESET_ALL}"

def save_working_links(links, output_file):
    with open(output_file, 'w') as file:
        for i, link in enumerate(links, start=1):
            status = check_link(link)
            file.write(f"{i}. {link} - {status}\n")

def process_links(links):
    working_links = []
    for i, link in enumerate(links, start=1):
        status = check_link(link)
        number_color = Fore.WHITE
        link_color = Fore.LIGHTBLUE_EX
        status_color = Fore.GREEN if "Working" in status else (Fore.RED if "Not working" in status else Fore.ORANGE)
        latency_color = Fore.LIGHTBLUE_EX
        if "Working" in status:
            status_split = status.split(" - ")
            print(f"{number_color}{i}. {Style.RESET_ALL}{link_color}{link}{Style.RESET_ALL} - {status_color}{status_split[0]}{Style.RESET_ALL} - {latency_color}{status_split[1]}{Style.RESET_ALL}")
            working_links.append(link)  # Append only if it's a working link
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
        if index <= len(links):
            webbrowser.open(links[index - 1])
        else:
            print(f"Invalid index: {index}")

try:
    # Read links from url.txt
    links = read_links_from_file('url.txt')

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
        additional_links = additional_links.split()  # Split the additional links string into separate links
        links.extend(additional_links)


    # Process the links
    working_links = process_links(links)

    # Save working links to works.txt
    save_working_links(working_links, 'works.txt')

    # Asks the user what to do with the working links
    print("\n\nWhat do you want to do?\n\n1. Open all links in browser (Only Working)\n\n2. Only open the links I want\n")
    
    while True:
        user_choice = keyboard.read_event(suppress=True).name
        if user_choice in ['1', '2']:
            break

    if user_choice == '1':
        for link in working_links:
            webbrowser.open(link)
    elif user_choice == '2':
        selected_indices = input("Select/choose links by giving corresponding number(s): ").strip()
        open_links_in_browser(working_links, selected_indices)
    else:
        print("Invalid choice. Please enter either 1 or 2.")

    # Print the demo text with random colors
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE]
    author = "This code was developed by Farhad Ahmed\nFor more information visit me at http://github.com/f4rh4d-4hmed"

    for _ in range(1):             #Number of times the author credit to show
        colored_text = ''.join(random.choice(colors) + char for char in author)
        print(colored_text)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nExitting:)")
