from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd

TIME_OUT = 80
MIN_FOLLOWERS = 1500


def string_to_num(string):
    string = string.strip(" Subscribers")
    if "K" in string or "k" in string:
        num_strip = string.strip("K").strip("k")
        num = float(num_strip) * 1000
    elif "M" in string or "m" in string:
        num_strip = string.strip("M").strip("m")
        num = float(num_strip) * 1000000
    elif "B" in string or "b" in string:
        num_strip = string.strip("B").strip("b")
        num = float(num_strip) * 1000000000
    else:
        num = int(string.replace(",", ""))
    return num


def go_through_tag_posts(tag):
    print("Running...")
    PATH = "/Users/paulrodriguez/Downloads/chromedriver"
    driver = webdriver.Chrome(PATH)
    # --------------------LOGIN---------------------
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

    # --------------------HASHTAG SEARCH---------------------

    # driver.get("https://www.instagram.com/explore/tags/" + tag)
    # first_post = "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a"
    # username = "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a"
    # next_button = "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button"
    #
    # try:
    #     element_present = EC.presence_of_element_located(
    #         (By.XPATH, first_post))
    #     WebDriverWait(driver, TIME_OUT).until(element_present)
    # except TimeoutException:
    #     print("Timed out looking for: First Post.")
    # driver.find_element(by=By.XPATH, value=first_post).click()
    # unbroken = True
    # while unbroken:
    #     try:
    #         element_present = EC.presence_of_element_located(
    #             (By.XPATH, username))
    #         WebDriverWait(driver, TIME_OUT).until(element_present)
    #     except TimeoutException:
    #         print("Timed out looking for: Username.")
    #         break
    #     post_username = driver.find_element(by=By.XPATH, value=username).text
    #     print(post_username)
    #     try:
    #         element_present = EC.presence_of_element_located(
    #             (By.XPATH, next_button))
    #         WebDriverWait(driver, TIME_OUT).until(element_present)
    #     except TimeoutException:
    #         print("Timed out looking for: Next Post Button.")
    #         break
    #     driver.find_element(by=By.XPATH, value=next_button).click()
    #
    #     with open('accounts.csv', 'a') as file:
    #         writer = csv.writer(file)
    #         writer.writerow([post_username])
    #         file.close()


    # --------------------USER SEARCH---------------------

    print("Finished going through the posts.")
    print("Configuring JSON for users")
    with open('accounts.csv', 'r') as fd:
        reader = csv.reader(fd)
        for username in reader:
            driver.get("https://www.instagram.com/" + username[0] + "/")

            try:
                element_present = EC.presence_of_element_located((By.XPATH,
                                                                  "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span"))
                WebDriverWait(driver, TIME_OUT).until(element_present)
            except TimeoutException:
                print("Timed out looking for: Instagram Followers.")
                break
            followers = driver.find_element(by=By.XPATH,
                                            value="/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span")
            followers_num = string_to_num(followers.text)
            print(followers_num)
            if followers_num > MIN_FOLLOWERS:
                new_data = [username[0], followers_num, tag]
                with open("quality_accounts.csv", 'a') as csv_file:
                    writer_object = csv.writer(csv_file)
                    writer_object.writerow(new_data)
                    csv_file.close()
                print("added " + username[0])
            else:
                print("deleted " + username[0])
    print("Finished!")

def sort_csv():
    df = pd.read_csv("quality_accounts.csv")
    df = df.drop_duplicates()
    print(df.head())
    sorted = df.sort_values(by=["followers"], ascending=False, ignore_index=True)
    sorted.to_csv("organized_accounts.csv")
    organized = pd.read_csv("organized_accounts.csv")
    return organized


#go_through_tag_posts("tbsinfluencers")
sort_csv()
