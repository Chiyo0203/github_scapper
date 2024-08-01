# src/main.py

from scraper import GitHubScraper
from config import TARGET_URL

def main():
    scraper = GitHubScraper()
    scraper.print_banner()
    given = input("GitHub profile URL: ")
    scraper.scrape(given)
    scraper.driver.quit()

if __name__ == "__main__":
    main()
