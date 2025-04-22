import webbrowser
from bs4 import BeautifulSoup
import requests
import platform
import os
import subprocess
from colorama import init as colorama_init
from colorama import Fore as color
from colorama import Style
import time
import sys
import socket
import pyfiglet

SUCCESS = int(200)
NOT_FOUND = int(404)

class Init1337x:
    MAIN_URL = "https://www.1377x.to/"

    def __init__(self, target, page):
        self.target = target
        self.page = page
        self.searchUrl = f"https://www.1377x.to/sort-search/{self.target}/seeders/desc/{self.page}"
        self.preDownloadLink = None
        self.downloadLink = None


def formatTarget(target):
    result = ""
    i = 0
    while i < len(target):
        if target[i] == ' ':
            result += '+'
        else:
            result += target[i]
        i += 1
    return result


def forWindows(obj):
    paths = [
        r"C:\Program Files\qBittorrent\qbittorrent.exe",
        r"C:\Program Files (x86)\qBittorrent\qbittorrent.exe"
    ]

    for path in paths:
        if os.path.exists(path):
            print(f"{color.GREEN}🔗 Magnet link: \n{obj.downloadLink}{Style.RESET_ALL}")
            time.sleep(2)
            subprocess.Popen([path, obj.downloadLink])
            return

    print(f"{color.RED}⚠️ qBittorrent not found in default install locations.{Style.RESET_ALL}")
    try:
        r = input("Do you want to install qBittorrent? (y/n): ")
        if r in ('y', 'Y'):
            webbrowser.open("https://www.fosshub.com/qBittorrent.html?dwl=qbittorrent_5.0.5_x64_setup.exe")
        else:
            print(f"{color.GREEN}Here’s your magnet link. For the best experience, it's recommended to have {Style.BRIGHT}qBittorrent{Style.NORMAL} installed:\n{obj.downloadLink}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("\n❌")
        time.sleep(1)
        sys.exit(1)
    except EOFError:
        print("\n❌")
        time.sleep(1)
        sys.exit(1)


def forLinux(obj):
    paths = [
        "/usr/bin/qbittorrent",
        "/opt/qbittorrent/qbittorrent",
        "/usr/local/bin/qbittorrent"
    ]

    for path in paths:
        if os.path.exists(path):
            print(f"{color.GREEN}🔗 Magnet link: \n{obj.downloadLink}{Style.RESET_ALL}")
            time.sleep(2)
            subprocess.Popen([path, obj.downloadLink])
            return

    print(f"{color.RED}⚠️ qBittorrent not found in default install locations.{Style.RESET_ALL}")
    try:
        r = input("Do you want to install qBittorrent? (y/n): ")
        if r in ('y', 'Y'):
            webbrowser.open("https://www.fosshub.com/qBittorrent.html?dwl=qbittorrent-linux-x64.tar.xz")
        else:
            print(f"{color.GREEN}Here’s your magnet link. For the best experience, it's recommended to have {Style.BRIGHT}qBittorrent{Style.NORMAL} installed:\n{obj.downloadLink}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("\n❌")
        time.sleep(1)
        sys.exit(1)
    except EOFError:
        print("\n❌")
        time.sleep(1)
        sys.exit(1)


def isInternetAvailable():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def main():
    
    osName = platform.system()
    colorama_init()
    flag = 0

    if not isInternetAvailable():
        print(f"{color.RED}⚠️ No internet connection detected. Please check your network settings and try again later.{Style.RESET_ALL}")
        time.sleep(1)
        return
    
    if osName == 'Darwin':
        print(f"{color.RED}🚫 This version is not compatible with macOS. Please use a supported platform.{Style.RESET_ALL}")
        time.sleep(1)
        return

    while True:
        
        if flag == 0:

            banner = pyfiglet.figlet_format("Magnetica")
            print(f"{color.CYAN}{Style.BRIGHT}{banner}{Style.RESET_ALL}")

            print(f"\n{color.CYAN}{Style.BRIGHT}🌟 Greetings, brave free spirit of the internet! 🌟{Style.RESET_ALL}")
            print(f"{color.GREEN}🔍 Dive in and discover the most reliable, working torrent links out there! 🚀{Style.RESET_ALL}\n")

            print(f"{color.CYAN}{Style.BRIGHT}Note:{Style.RESET_ALL} "
                f"{color.YELLOW}You must have {Style.BRIGHT}qBittorrent{Style.NORMAL}{color.YELLOW} installed on your PC. "
                f"{color.GREEN}Using open source software is a must!{Style.RESET_ALL}")

        if flag >= 1:
            try:
                r = input(f"{color.YELLOW}🔁 Wanna fetch more torrent links? (y/n): {Style.RESET_ALL}")
                if r in ('y', 'Y'):
                    pass
                else:
                    print(f"{color.RED}👋 Exiting the program. Don’t be a stranger — come back soon for more! 🚀{Style.RESET_ALL}")
                    time.sleep(1)
                    break
            except KeyboardInterrupt:
                print("\n❌")
                time.sleep(1)
                sys.exit(1)
            except EOFError:
                print("\n❌")
                time.sleep(1)
                sys.exit(1)

        try:
            while True:
                target = input(f"{color.CYAN}Find torrents — just enter a keyword: {Style.RESET_ALL}")
                target = target.strip()
                if not target:
                    continue
                break
            
            page = 1

            if target:
                target = formatTarget(target)
                obj = Init1337x(target, page)
                response = requests.get(obj.searchUrl)
                if response.status_code == SUCCESS:
                    parsedHtml = BeautifulSoup(response.text, 'html.parser')
                    
                    td = parsedHtml.find('td')
                    if td is not None:
                        a = td.find_all('a')
                    else:
                        print(f"{color.RED}❌ Error: The content you are looking for does not exist!{Style.RESET_ALL}")
                        return
                    obj.preDownloadLink = obj.MAIN_URL.rstrip('/') + a[1].get('href')
                    
                    response = requests.get(obj.preDownloadLink)
                    if response.status_code == SUCCESS:
                        parsedHtml = BeautifulSoup(response.text, 'html.parser')

                        mainTag = parsedHtml.find('main')
                        if mainTag is not None:
                            torrentLinks = mainTag.select('li > a[class^="torrentdown1"]')
                            for a in torrentLinks:
                                obj.downloadLink = a['href']
                        else:
                            print(f"{color.RED}❌ Error: The content you are looking for does not exist!{Style.RESET_ALL}")
                            return
                        if osName == 'Windows':
                            forWindows(obj)
                        elif osName == 'Linux':
                            forLinux(obj)
                elif response.status_code == NOT_FOUND:
                    print(f"{color.RED}❌ Error: Link may be broken!{Style.RESET_ALL}")
            else:
                print(f"{color.RED}⚠️ Error: Nothing has been entered!{Style.RESET_ALL}")
            flag += 1
        except KeyboardInterrupt:
            print("\n❌")
            time.sleep(1)
            sys.exit(1)
        except EOFError:
            print("\n❌")
            time.sleep(1)
            sys.exit(1)
    
if __name__ == "__main__":
    main()
