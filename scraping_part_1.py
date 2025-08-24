from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
driver = webdriver.Chrome()
driver.get("https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc")
wait = WebDriverWait(driver, 10)

## Clicking all the loading button at the bottom of the page
load_button_xpath = '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button'
clicked = 0
while True:
    try:
        button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, load_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", button)
        print(f"Button clicked successfully. Total: {clicked+1}")
        clicked += 1
        time.sleep(1)
    except Exception:
        print("No more 'Show 50 more' buttons found or all titles loaded.")
        break
print(f"All 'Show 50 more' buttons clicked. Total: {clicked}")

## going to top of the page
driver.execute_script("window.scrollTo(0, 0);")

i_button_xpath='//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[{}]/div/div/div/div[1]/div[3]/button'
try:
    for i in range(1, 251):
        button = wait.until(EC.presence_of_element_located((By.XPATH, i_button_xpath.format(i))))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div"))
        )
        popup_html = popup.get_attribute("outerHTML")
        with open(f"scrap/popup{i}.html", "w", encoding="utf-8") as f:
            f.write(popup_html)
        time.sleep(1)
        close_button_xpath='/html/body/div[4]/div[2]/div/div[1]/button'
        close_button = wait.until(EC.presence_of_element_located((By.XPATH, close_button_xpath)))
        time.sleep(1)
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(1)
    print("All popups saved for 250 titles.")
except Exception as e:
    print(f"Error while clicking button: {e}")

driver.quit()