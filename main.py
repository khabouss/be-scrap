from colorama import Fore
from bs4 import BeautifulSoup
from helpers import REDIS_PORT, REDIS_URL, REDIS_DB,\
    REDIS_QUEUE, get_content, site_maps, update_ui, client,\
    get_pages
import json
import time
import csv

def main():
    prog = 0
    pages = get_pages(0, -1)
    print(Fore.GREEN + "FOUND "+str(len(pages))+" PAGES"+ Fore.RESET)
    with open("results.csv", 'w', newline='') as f:
        w = csv.DictWriter(f, ['company_website', 'company_id'])
        w.writeheader()
        for page in pages:
            time.sleep(1)
            content = get_content(str(page))
            soup = BeautifulSoup(content.content, features="html.parser")
            next_data = soup.find("script", attrs={"id": "__NEXT_DATA__"})
            if next_data is None:
                continue
            loads = json.loads(next_data.text)
            info = {}
            info["company_website"] = loads['props']['pageProps']['companySubheader']['websiteUrl']
            info["company_id"] = loads['props']['pageProps']['companyAbout']['registrationNumber']
            if info["company_website"] is None or info["company_id"] is None:
                continue
            w.writerow(info)
            update_ui(prog)
            prog += 1
    print(Fore.YELLOW + "-- THE END --" + Fore.RESET)


if __name__ == "__main__":
    main()
