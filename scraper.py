import time


class ScrapingResult:
    def __init__(self):
        self.url = None
        self.summary = None


LANGUAGE = "english"
SENTENCES_COUNT = 2


class Scraper:
    def scrape(self, url):
        time.sleep(10)
        print(url)
        scraping_result = ScrapingResult()

        scraping_result.summary = url
        scraping_result.url = url

        print("sleep 10:")
        return scraping_result
