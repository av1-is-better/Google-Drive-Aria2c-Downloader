#!/home/ubuntu/venv/bin/python

import requests
import re
import os
from colorama import Fore, Style

print(Style.BRIGHT + Fore.LIGHTCYAN_EX + '''

░██████╗░░█████╗░░█████╗░░██████╗░██╗░░░░░███████╗  ██████╗░██████╗░██╗██╗░░░██╗███████╗
██╔════╝░██╔══██╗██╔══██╗██╔════╝░██║░░░░░██╔════╝  ██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
██║░░██╗░██║░░██║██║░░██║██║░░██╗░██║░░░░░█████╗░░  ██║░░██║██████╔╝██║╚██╗░██╔╝█████╗░░
██║░░╚██╗██║░░██║██║░░██║██║░░╚██╗██║░░░░░██╔══╝░░  ██║░░██║██╔══██╗██║░╚████╔╝░██╔══╝░░
╚██████╔╝╚█████╔╝╚█████╔╝╚██████╔╝███████╗███████╗  ██████╔╝██║░░██║██║░░╚██╔╝░░███████╗
░╚═════╝░░╚════╝░░╚════╝░░╚═════╝░╚══════╝╚══════╝  ╚═════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚══════╝''')
print(Style.BRIGHT + Fore.GREEN + '''
                      █▀▄ █▀█ █░█░█ █▄░█ █░░ █▀█ ▄▀█ █▀▄ █▀▀ █▀█
                      █▄▀ █▄█ ▀▄▀▄▀ █░▀█ █▄▄ █▄█ █▀█ █▄▀ ██▄ █▀▄
''')


def extract_uuid_and_filename(drive_file_id):
    url = f"https://drive.google.com/uc?export=download&id={drive_file_id}"
    
    session = requests.Session()
    response = session.get(url)
    
    # Extract UUID
    uuid_match = re.search(r'name="uuid" value="([a-f0-9\-]+)"', response.text)
    uuid_value = uuid_match.group(1) if uuid_match else None

    # Extract Filename
    filename_match = re.search(r'<a href="\/open\?id=.*?">(.*?)<\/a>', response.text)
    filename = filename_match.group(1) if filename_match else None

    return uuid_value, filename

def extract_drive_id(url):
    pattern = r'(?:id=|/d/|file/d/|open\?id=)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Checking aria2c
exit_code = os.system("aria2c --help > /dev/null 2>&1")
if exit_code != 0:
    print(Fore.LIGHTRED_EX + "\nError: aria2c not found in your system. Exiting..."+ Style.RESET_ALL)
    exit(1)

# Google Drive File ID
drive_file_id = extract_drive_id(input(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "Enter File URL: " + Fore.LIGHTBLUE_EX))

# Download Folder Path
download_dir = "/home/ubuntu/downloads"


uuid_value, file_name = extract_uuid_and_filename(drive_file_id)


# checking file id
if not drive_file_id:
    print(Fore.LIGHTRED_EX + "\nError: File ID not present in provided URL. Exiting..."+ Style.RESET_ALL)
    exit(1)

# checking uuid
if uuid_value:
    print(Style.BRIGHT + Fore.YELLOW + "\nDownload UUID: " + Style.BRIGHT + Fore.LIGHTMAGENTA_EX + f"{uuid_value}" + Style.RESET_ALL)
else:
    print(Fore.LIGHTRED_EX + "\nError: UUID not found in the HTML response" + Style.RESET_ALL)
    exit(1)

# checking file_name
if file_name:
    print(Style.BRIGHT + Fore.YELLOW + "File Name: " + Style.BRIGHT + Fore.GREEN + f"{file_name}" + Style.RESET_ALL)
else:
    print(Fore.LIGHTRED_EX + "\nError: File Name not found in the HTML response" + Style.RESET_ALL)
    exit(1)

print(Style.BRIGHT + Fore.YELLOW + "Download Path: " + Style.BRIGHT + Fore.LIGHTCYAN_EX + f"{download_dir}" + Style.RESET_ALL)


print(Style.BRIGHT + Fore.GREEN +'\n=========================================================================')
print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "                          Download Started  ")
print(Style.BRIGHT + Fore.GREEN +'=========================================================================\n'+ Style.RESET_ALL)

os.system(f'''aria2c \\
    -x4 \\
    -d {download_dir} \\
    --file-allocation=none \\
    --summary-interval=0 \\
    --console-log-level=error \\
    --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0" \\
    "https://drive.usercontent.google.com/download?id={drive_file_id}&export=download&authuser=0&confirm=t&uuid={uuid_value}"
    ''')
