from redis import Redis
from colorama import Fore
from bs4 import BeautifulSoup
from helpers import REDIS_PORT
from helpers import REDIS_URL
from helpers import REDIS_DB
from helpers import REDIS_QUEUE
from helpers import get_content
from helpers import site_maps
import json
import time
from helpers import update_ui

client = Redis(REDIS_URL, REDIS_PORT, REDIS_DB)



def main():
    prog = 0
    for site_map in site_maps:
        with open(site_map, "r") as f:
            data = f.read()
            f.close()
            soup = BeautifulSoup(data, "xml")
            url_tag = soup.find("urlset").find_all("url")
            for url in url_tag:
                page = url.find("loc").text
                time.sleep(1)
                content = get_content(page)
                soup = BeautifulSoup(content.content, features="html.parser")
                next_data = soup.find("script", attrs={"id": "__NEXT_DATA__"})
                if next_data is None:
                    continue
                loads = json.loads(next_data.text)
                website = loads['props']['pageProps']['companySubheader']['websiteUrl']
                company_id = loads['props']['pageProps']['companyAbout']['registrationNumber']
                if website is None or company_id is None:
                    continue
                client.rpush(REDIS_QUEUE, json.dumps(
                    {"website": website, "company_id": company_id}))
                update_ui(prog)
    print(Fore.YELLOW + "-- THE END --" + Fore.RESET)


if __name__ == "__main__":
    main()
