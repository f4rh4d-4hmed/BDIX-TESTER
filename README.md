# BDIX-TESTER-PY

BDIX-TESTER is a Python script that checks the status of multiple URLs. It reads the links from a file (`url.txt`), checks their availability, and saves the working links to another file (`works.txt`). Additionally, it provides options to open the working links in a web browser.
<img width="766" height="267" alt="image" src="https://github.com/user-attachments/assets/404d44fa-c83a-4ca2-a53a-73d9f8132beb" />


# Windows [Click Here](https://github.com/f4rh4d-4hmed/BDIX-TESTER/releases/download/v0.2.2/BDIX-TESTER-v0.2.2.zip)
## Termux
Follow menual installation from source code
## Installation

1. Clone the repository or download the source code.
```
git clone https://github.com/f4rh4d-4hmed/BDIX-TESTER
```
```
cd BDIX-TESTER
```
2. Make sure you have Python 3.x installed on your system.
3. Install the required dependencies by running the following command in your terminal or command prompt:

```
pip install -r requirements.txt
```

## Build
To build it yourself-
```
python3 setup.py build
```
Should work on linix as well (recommanded to use directly from source code)
## Usage
1. Run the script by executing the following command in your terminal or command prompt:

```
python3 main.py
```

2. The script will display a colorful greeting and prompt you to enter additional links (if any). If you don't have any additional links, simply press Enter.
3. The script will start checking the links and display their status (Working, Not working, or May contain threat) along with the response time for working links.
4. After checking all the links, the script will save the working links to the `works.txt` file.
5. You will be prompted with two options:
   - Option 1: Open all working links in your default web browser.
   - Option 2: Open specific links by providing their corresponding numbers.

6. Make your choice by entering the appropriate number (1 or 2).
   - If you choose Option 1, all working links will open in your default web browser.
   - If you choose Option 2, you will be prompted to enter the numbers of the links you want to open, separated by commas (e.g., `1,3,5-7`).

7. Finally, the script will exit.

## Features

- Checks the status of multiple URLs.
- Supports HTTP and HTTPS protocols.
- Displays the response time for working links.
- Saves the working links to a file (`works.txt`) for later use.
- Provides options to open the working links in a web browser.
- Handles keyboard interrupts gracefully.
- Colorful output for better visibility.

## Dependencies

The script requires the following Python packages:

- `requests`: For making HTTP requests to check the links.
- `colorama`: For adding color to the output text.

These dependencies are listed in the `requirements.txt` file and can be installed using the provided command.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements and new bdix links, please open an issue or submit a pull request.
## Current contributors
<a herf="https://github.com/f4rh4d-4hmed/BDIX-TESTER/graphs/contributors"><img src="https://contrib.rocks/image?repo=f4rh4d-4hmed/BDIX-TESTER" />
</a>
## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Check out my other repo
