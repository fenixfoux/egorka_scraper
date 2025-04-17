from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from one_item import Item
# temporary collected and separated links (later this one will be done by a function)
from temp_links import collected_links_cactus, collected_links_bomba

import time
import re

LOAD_TIME = 5

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')  # removes the "controlled" message
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

options.add_argument('--headless')  # run in bacground without open browser
options.add_argument('--disable-gpu')  # improves headless stability


driver = webdriver.Chrome(service=service, options=options)

# disable webdriver flag in JS
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """
})


def bomba_scrap(rec_driver: webdriver.Chrome, load_time: time, links_list):
    bomba_objects = []
    for one_link in links_list:
        rec_driver.get(one_link)
        time.sleep(2)

        name_elem = rec_driver.find_element(By.CSS_SELECTOR, 'div.header__title > h1')
        price_elem = rec_driver.find_element(By.CSS_SELECTOR, "span.product-panel__price")

        item = Item()
        item.name = name_elem.text.strip()
        item.price = int(re.sub(r"[^\d]", "", price_elem.text.strip().replace(" ", "")))

        print(f"item.name: {item.name}")
        print(f"item.price: {item.price}")
        print(f"====")




def cactus_scrap(rec_driver: webdriver.Chrome, load_time: time, links_list):
    cactus_objects = []
    for one_link in links_list:
        rec_driver.get(one_link)
        time.sleep(load_time)

        name_elem = rec_driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]')
        price_elem = rec_driver.find_element(By.CSS_SELECTOR,
                                             'span.catalog__item__prices__actual__val[itemprop="price"]')

        item = Item()
        item.name = name_elem.text.strip()
        item.price = int(re.sub(r"[^\d]", "", price_elem.text.strip().replace(" ", "")))
        # print(f"collected item data:\nitem.name: {item.name}\nitem.price: '{str(item.price)}'")

        # modal window part
        try:
            credit_button = rec_driver.find_element(By.CSS_SELECTOR, 'div#ctl00_cphMain_divBestCredit')
            credit_button.click()

            WebDriverWait(rec_driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"].show'))
            )
            print("credit popup is open")

            # Wait until the <select> has loaded its <option> elements
            WebDriverWait(rec_driver, 5).until(
                lambda driver: len(driver.find_element(By.CSS_SELECTOR, 'select.custom-select')
                                   .find_elements(By.TAG_NAME, 'option')) > 0
            )

            # Now safely get the select element
            select_elem = rec_driver.find_element(By.CSS_SELECTOR, 'select.custom-select')

            # Get all option elements
            option_elements = select_elem.find_elements(By.TAG_NAME, "option")

            # Print each value
            for opt in option_elements:
                val = opt.get_attribute("value")
                txt = opt.text.strip()
                print(f"📦 Option -> value: '{val}', text: '{txt}'")

            # # Now locate the <select> element
            # select_elem = rec_driver.find_element(By.CSS_SELECTOR, 'select.custom-select')
            # # print(f"select_elem: {select_elem}")
            #
            # # Now grab ALL the <option> tags inside the <select>
            # # time.sleep(7)
            # option_elements = select_elem.find_elements(By.TAG_NAME, "option")
            # print("Total options found:", len(option_elements))
            # #
            # # Print their text + value
            # for opt in option_elements:
            #     val = opt.get_attribute("value")
            #     txt = opt.text.strip()
            #     print(f"📦 Option -> value: '{val}', text: '{txt}'")

            # for _ in select_elem.find_elements(By.TAG_NAME, 'option'):
            #     print(f"found option: {_}")

            # # Grab all <option> elements inside
            # option_elements = select_elem.find_elements(By.TAG_NAME, 'option')
            #
            # # Extract their 'value' attributes
            # # option_values = [opt.get_attribute("value") for opt in option_elements if opt.get_attribute("value")]
            # option_values = [opt.get_dom_attribute("value") for opt in option_elements if opt.get_dom_attribute("value")]
            #
            # print("Option values found:", option_values)


        except Exception as e:
            print(f"Failed to open popup or change option: {e}")

        cactus_objects.append(item)

    rec_driver.quit()
    return cactus_objects


bomba_scrap(rec_driver=driver, load_time=5, links_list=collected_links_bomba)

# cactus_scraped_list_objects = cactus_scrap(rec_driver=driver, load_time=LOAD_TIME, links_list=collected_links_cactus)
# print(cactus_scraped_list_objects)
"""

     
"""
