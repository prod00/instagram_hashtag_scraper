from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIME_OUT = 80


def go_through_tag_posts(tag):
    print("Running...")
    PATH = "/Users/paulrodriguez/Downloads/chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.instagram.com/accounts/login/")
    try:
        element_present = EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input"))
        WebDriverWait(driver, TIME_OUT).until(element_present)
    except TimeoutException:
        print("Timed out looking for: Username Box.")
    driver.find_element(by=By.XPATH,
                        value="/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input").send_keys(
        "thenerdsong")
    driver.find_element(by=By.XPATH, value="//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(
        "DontForgetThisWill")
    driver.find_element(by=By.XPATH, value="//*[@id='loginForm']/div/div[3]/button").click()
    time.sleep(4)

    driver.get("https://www.instagram.com/explore/tags/" + tag)
    first_post = "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a"
    username = "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a"
    next_button = "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button"

    try:
        element_present = EC.presence_of_element_located(
            (By.XPATH, first_post))
        WebDriverWait(driver, TIME_OUT).until(element_present)
    except TimeoutException:
        print("Timed out looking for: First Post.")
    driver.find_element(by=By.XPATH, value=first_post).click()

    while True:
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, username))
            WebDriverWait(driver, TIME_OUT).until(element_present)
        except TimeoutException:
            print("Timed out looking for: Username.")
        post_username = driver.find_element(by=By.XPATH, value=username).text
        print(post_username)
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, next_button))
            WebDriverWait(driver, TIME_OUT).until(element_present)
        except TimeoutException:
            print("Timed out looking for: Next Post Button.")
        driver.find_element(by=By.XPATH, value=next_button).click()

        with open('accounts.txt', 'a') as file:
            file.write(post_username + "\n")


tag = input("Enter Desired Hashtag: ")
go_through_tag_posts(tag)
