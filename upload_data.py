from colorama import Fore
from bs4 import BeautifulSoup
from helpers import REDIS_QUEUE, site_maps, update_ui, client

def get_last_value():
    data = client.lrange(REDIS_QUEUE, 0, -1)
    return data[-1]

def push_site_maps():
    prog = 0
    last = get_last_value()
    begin = False
    for site_map in site_maps:
        with open(site_map, "r") as f:
            data = f.read()
            f.close()
            soup = BeautifulSoup(data, "lxml")
            url_tag = soup.find("urlset").find_all("url")
            for url in url_tag:
                if begin == False:
                    if url != last:
                        continue
                    else:
                        begin = True
                        continue
                page = url.find("loc").text
                client.rpush(REDIS_QUEUE, page)
                update_ui(prog)
                prog += 1

if __name__ == "__main__":
    push_site_maps()
