# src/scraper.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from .config import CHROME_DRIVER_PATH, TARGET_URL

# try adding path of your chromedriver instead of importing from config
chrome_driver_path = r"D:\HP\chromedriver-win64\chromedriver-win64\chromedriver.exe"

class GitHubScraper:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
    
    def print_banner(self):
        banner = """
                      .-') _    ('-. .-.            .-. .-')          .-')              _  .-')     ('-.      _ (`-.    _ (`-.    ('-.  _  .-')   
                    (  OO) )  ( OO )  /            \  ( OO )        ( OO ).           ( \( -O )   ( OO ).-. ( (OO  )  ( (OO  ) _(  OO)( \( -O )  
  ,----.     ,-.-') /     '._ ,--. ,--. ,--. ,--.   ;-----.\       (_)---\_)   .-----. ,------.   / . --. /_.`     \ _.`     \(,------.,------.  
 '  .-./-')  |  |OO)|'--...__)|  | |  | |  | |  |   | .-.  |       /    _ |   '  .--./ |   /`. '  | \-.  \(__...--''(__...--'' |  .---'|   /`. ' 
 |  |_( O- ) |  |  \'--.  .--'|   .|  | |  | | .-') | '-' /_)      \  :` `.   |  |('-. |  /  | |.-'-'  |  ||  /  | | |  /  | | |  |    |  /  | | 
 |  | .--, \ |  |(_/   |  |   |       | |  |_|( OO )| .-. `.        '..`''.) /_) |OO  )|  |_.' | \| |_.'  ||  |_.' | |  |_.' |(|  '--. |  |_.' | 
(|  | '. (_/,|  |_.'   |  |   |  .-.  | |  | | `-' /| |  \  |      .-._)   \ ||  |`-'| |  .  '.'  |  .-.  ||  .___.' |  .___.' |  .--' |  .  '.' 
 |  '--'  |(_|  |      |  |   |  | |  |('  '-'(_.-' | '--'  /      \       /(_'  '--'\ |  |\  \   |  | |  ||  |      |  |      |  `---.|  |\  \  
  `------'   `--'      `--'   `--' `--'  `-----'    `------'        `-----'    `-----' `--' '--'  `--' `--'`--'      `--'      `------'`--' '--' 
  
    """
        print(banner)

    def go_to_raw(self, sec_page):
        raw_element = self.driver.find_element(By.XPATH, "//a[@data-testid='raw-button']//span[text()='Raw']")
        raw_element.click()
        time.sleep(3)
        html = self.driver.page_source
        print(html)
        if "nothing" in html:
            print(f"pass in this file {sec_page}")

    def loop(self, next_page):
        self.driver.get(next_page)
        res2 = self.driver.find_elements(By.CLASS_NAME, "Link--primary")

        tlink = [b.text for b in res2]
        slink = [p for p in tlink if 'html' in p or 'py' in p or 'txt' in p]

        print(slink)
        for s in slink:
            sec2_page = f"{next_page}/tree/main/{s}"
            sec_page = f"{next_page}/blob/main/{s}"

            try:
                self.driver.get(sec_page)
            except:
                self.driver.get(sec2_page)
                self.loop(sec2_page)
                
            time.sleep(4)
            self.go_to_raw(sec_page)

    def scrape(self, website):
        self.driver.get(website)
        res = self.driver.find_elements(By.CLASS_NAME, "repo")
        link = [i.text for i in res if i.text != "kalkithegodsagar"]
        flink = []

        for l in link:
            next_page = f"{website}/{l}"
            flink.append(next_page)
            self.loop(next_page)

        print(flink)
