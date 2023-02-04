from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from config.config import PATH_TO_CHROMEDRIVER


def connection():
  PATH = PATH_TO_CHROMEDRIVER
  options = Options()
  options.binary_location = "/usr/lib/chromium-browser/chromium-browser"
  driver = webdriver.Chrome(PATH, chrome_options=options)
  return driver

def get_search_suggestions(search_term):
  driver = connection()
  driver.get("https://youtube.com")


  wait = WebDriverWait(driver, 10)
  try:
    search = wait.until(
      EC.presence_of_element_located((By.NAME, "search_query"))
    )

    if len(search_term) > 1:

      search.send_keys(search_term[0])
      time.sleep(5)
      search.send_keys(search_term[1:])

      time.sleep(10)

      sugestions = driver.find_element_by_xpath("//ul[@role='listbox']")
      html_content = sugestions.get_attribute('outerHTML')

      soup = BeautifulSoup(html_content, 'html.parser')

      sug_list = list(soup.ul)

      results = list()

      for item in sug_list:
        soup = BeautifulSoup(str(item), 'html.parser')
        r = soup.li.div.find_all('div', class_='sbqs_c')

        cleantext = BeautifulSoup(str(r), 'html.parser').text
        x = re.sub('([\[\]]+)', '', cleantext)
        results.append(x)

      time.sleep(5)

      driver.close()

      return results

    else:
      return {"message": "Search term too short"}

  except Exception as e:
    print("ERRO")
    print(e)
