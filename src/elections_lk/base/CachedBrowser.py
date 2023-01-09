from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils.cache import cache


class CachedBrowser:
    def __init__(self):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        print('Opened browser.')
        self.browser = browser

    def quit(self):
        self.browser.close()
        self.browser.quit()
        print('Quit browser.')

    def getSource(self, url):
        @cache('get_source', 86400)
        def inner(url):
            print(f'Getting source form "{url}"')
            self.browser.get(url)
            return self.browser.page_source

        return inner(url)
