from selenium import webdriver
import time
browser = webdriver.Chrome("/home/sparkle/Chess/chromedriver")
browser.get('https://www.chess.com/games/mikhail-botvinnik')

any_page_left = True

while any_page_left:
    checkboxes = browser.find_elements_by_class_name("master-games-checkbox")
    download = browser.find_element_by_class_name("master-games-download-button")

    try:
        nextpage = browser.find_element_by_class_name("pagination-next")
    except:
        any_page_left = False

    for i in range(len(checkboxes)):
        time.sleep(0.2)
        checkboxes[i].click()
        time.sleep(0.2)
        checkboxes[i-1].click() if i > 0 else None
        time.sleep(0.2)
        download.click()

    if i == len(checkboxes) - 1 and any_page_left:
        nextpage.click()
        time.sleep(2)
