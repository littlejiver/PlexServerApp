from qbittorrent import Client

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

import os

running = True
while running:
    print("PlexServerApp Alpha v0.001a\n")
    print("Please report all bugs to Simon!")
    print("________________________________________")
    print("What would you like to do?:\n")
    print("1 - Download Movie")
    print("2 - Download and/or Monitor a Series")
    print("q - Exit")

    task = input("What would you like to do?: ")

    if task == "1":
        found = False
        movieName = input("What movie would you like? (full or partial names excepted): ")
        for root, dirs, files in os.walk("/home/littlejiver/PlexContent/Movies"):
            for file in files:
                if movieName in file:
                    print("Found: " + file + " already on plex server!")
                    if "y" in input("Is this the right movie? (y/n): "):
                        found = True
                    else:
                        print("try to be more specific!")
        if not found:
            options = Options()
            options.add_argument("--headless")  # Runs Chrome in headless mode.
            options.add_argument('--no-sandbox')  # # Bypass OS security model
            options.add_argument('start-maximized')
            options.add_argument('disable-infobars')
            options.add_argument("--disable-extensions")
            driver = webdriver.Chrome(chrome_options=options,
                                         executable_path='/home/littlejiver/Downloads/chromedriver_linux64/chromedriver')

            # driver = webdriver.Chrome(executable_path=
            #                           r'/home/littlejiver/Downloads/chromedriver_linux64/chromedriver')
            driver.get("https://imdb.com/")

            wait = WebDriverWait(driver, 10)
            wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="suggestion-search"]'))).send_keys(movieName)
        try:
            imdbMovieTitleResult = wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[1]'))
            ).text
            imdbMovieYearResult = wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[2]'))
            ).text
            imdbMovieStarsResult = wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[3]'))
            ).text

            print("Movie Title: " + imdbMovieTitleResult)
            print("Movie Year: " + imdbMovieYearResult)
            print("Movie Stars: " + imdbMovieStarsResult)

            if "n" in input("is this the right movie? (y/n): "):
                continue
            else:
                print("Checking Zoogle.com!")
                driver.get("https://www.zooqle.com/")
                wait.until(ec.element_to_be_clickable(
                    (By.XPATH, '//div[@id="anp2-wrapper"]//div[text()="NO THANKS"]'))).click()
                wait.until(
                            ec.element_to_be_clickable((By.XPATH, '//input[@name="q"]'))
                           ).send_keys(imdbMovieTitleResult)

                searchBar = wait.until(ec.element_to_be_clickable((By.XPATH, '//div[@class="tt-dataset tt-datas'
                                                                   + 'et-qs"]//p[@class="tt-wrap tt-suggestion '
                                                                   + 'tt-selectable"]//span[text()="'
                                                                   + imdbMovieTitleResult + '"]')))
                searchBar.click()
                wait.until(ec.element_to_be_clickable(
                    (By.XPATH,
                        '//*[@id="body_container"]/div/div[1]/div[2]/div/table/tbody/tr[2]/td[2]/a'))).click()
                magnetLink = wait.until(ec.element_to_be_clickable(
                                                            (By.XPATH, '//*[@id="dlPanel"]/div[2]/ul/li[2]/a')))
                torrentLink = magnetLink.get_attribute("href")
                qb = Client("http://127.0.0.1:8080/")
                qb.login("admin", "adminadmin")
                qb.download_from_link(torrentLink)
                print("Movie Found on Zoogle.com! Downloading now!, Please contact Simon to find out when finished")

        except:
            print("Movie Not Found!")

            driver.close()

    if task == "2":
        print("sorry, still under construction!")

    if task == "q":
        running = False
