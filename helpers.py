import random
import requests
from colorama import Fore
import sys
import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL   = os.getenv("REDIS_URL")
REDIS_PORT  = os.getenv("REDIS_PORT")
REDIS_DB    = os.getenv("REDIS_DB")
REDIS_QUEUE = os.getenv("REDIS_QUEUE")

client = Redis(REDIS_URL, REDIS_PORT, REDIS_DB)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

proxies = ['69.30.240.226:15005', '69.30.197.122:15005', '173.208.239.10:15005', '173.208.136.2:15005', '69.30.240.226:15006', '69.30.197.122:15006', '173.208.239.10:15006', '173.208.136.2:15006', '69.30.240.226:15007', '69.30.197.122:15007', '173.208.239.10:15007', '173.208.136.2:15007', '69.30.240.226:15008', '69.30.197.122:15008', '173.208.239.10:15008', '173.208.136.2:15008',
           '195.154.255.118:15005', '195.154.222.228:15005', '195.154.255.34:15005', '195.154.222.26:15005', '195.154.255.118:15006', '195.154.222.228:15006', '195.154.255.34:15006', '195.154.222.26:15006', '195.154.255.118:15007', '195.154.222.228:15007', '195.154.255.34:15007', '195.154.222.26:15007', '195.154.255.118:15008', '195.154.222.228:15008', '195.154.255.34:15008', '195.154.222.26:15008']

site_maps = [
    "data/sitemap.companies.be-en.1.xml",
    "data/sitemap.companies.be-en.2.xml",
    "data/sitemap.companies.be-en.3.xml",
    "data/sitemap.companies.be-en.4.xml",
    "data/sitemap.companies.be-en.5.xml",
    "data/sitemap.companies.be-en.6.xml",
    "data/sitemap.companies.be-en.7.xml",
    "data/sitemap.companies.be-en.8.xml",
    "data/sitemap.companies.be-en.9.xml",
    "data/sitemap.companies.be-en.10.xml",
    "data/sitemap.companies.be-en.11.xml",
    "data/sitemap.companies.be-en.12.xml",
    "data/sitemap.companies.be-en.13.xml",
    "data/sitemap.companies.be-en.14.xml",
    "data/sitemap.companies.be-en.15.xml",
    "data/sitemap.companies.be-en.16.xml",
    "data/sitemap.companies.be-en.17.xml",
    "data/sitemap.companies.be-en.18.xml",
    "data/sitemap.companies.be-en.19.xml",
    "data/sitemap.companies.be-en.20.xml",
    "data/sitemap.companies.be-en.21.xml",
    "data/sitemap.companies.be-en.22.xml",
    "data/sitemap.companies.be-en.23.xml",
    "data/sitemap.companies.be-en.24.xml",
    "data/sitemap.companies.be-en.25.xml",
    "data/sitemap.companies.be-en.26.xml",
    "data/sitemap.companies.be-en.27.xml",
    "data/sitemap.companies.be-en.28.xml",
    "data/sitemap.companies.be-en.29.xml",
    "data/sitemap.companies.be-en.30.xml",
    "data/sitemap.companies.be-en.31.xml",
    "data/sitemap.companies.be-en.32.xml",
    "data/sitemap.companies.be-en.33.xml",
    "data/sitemap.companies.be-en.34.xml",
    "data/sitemap.companies.be-en.35.xml",
    "data/sitemap.companies.be-en.36.xml",
    "data/sitemap.companies.be-en.37.xml",
    "data/sitemap.companies.be-en.38.xml",
    "data/sitemap.companies.be-en.39.xml",
    "data/sitemap.companies.be-en.40.xml",
    "data/sitemap.companies.be-en.41.xml",
    "data/sitemap.companies.be-en.42.xml",
    "data/sitemap.companies.be-en.43.xml",
    "data/sitemap.companies.be-en.44.xml",
    "data/sitemap.companies.be-en.45.xml",
    "data/sitemap.companies.be-en.46.xml",
    "data/sitemap.companies.be-en.47.xml",
    "data/sitemap.companies.be-en.48.xml",
    "data/sitemap.companies.be-en.49.xml",
    "data/sitemap.companies.be-en.50.xml",
    "data/sitemap.companies.be-en.51.xml",
    "data/sitemap.companies.be-en.52.xml"
]


def get_next():
    return random.randint(0, len(proxies))

def get_pages(start, end):
    return client.lrange(REDIS_QUEUE, start, end)

def get_content(page):
    content = None
    while content is None:
        proxy_id = get_next()
        try:
            # proxies={"http":proxies[proxy_id], "https":proxies[proxy_id]}
            content = requests.get(page, proxies={"http":proxies[proxy_id], "https":proxies[proxy_id]},headers=headers)
        except:
            print(Fore.BLUE + "Connection failed, changing proxy.." + Fore.RESET)
    return content

def update_ui(current_prog):
    """
        print the current progress to the terminal output
        :param current_prog: the current progress to print
        :type current_prog: number
    """
    sys.stdout.write("\r{0}>".format("="*2))
    sys.stdout.write("\033[92m CURRENT PROGRESS: \033[0m")
    sys.stdout.write(" "+str(current_prog))
    sys.stdout.flush()
