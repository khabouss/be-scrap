from colorama import Fore
from bs4 import BeautifulSoup
from helpers import REDIS_PORT, REDIS_URL, REDIS_DB,\
    REDIS_QUEUE, get_content, site_maps, update_ui, client,\
    get_pages
import json
import time


def main():
    prog = 0
    pages = get_pages(0, -1)
    for page in pages:
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
