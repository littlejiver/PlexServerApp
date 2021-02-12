from django.shortcuts import render

from qbittorrent import Client
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from movies.task import torrent_downloading_progress

import os


temp = ["You shouldn't see this"]
torrents = []


def index(request):
    return render(request, "movies/index.html")


def result(request):
    res = request.GET['ans']

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # # Bypass OS security model
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options=options, executable_path=
    r'/home/littlejiver/Downloads/chromedriver_linux64/chromedriver'
                              )
    wait = WebDriverWait(driver, 10)

    # driver = webdriver.Chrome(executable_path=r'/home/littlejiver/Downloads/chromedriver_linux64/chromedriver')
    driver.get("https://www.imdb.com")
    # wait = WebDriverWait(driver, 10)
    wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="suggestion-search"]'))).send_keys(res)

    imdbMovieTitleResult = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[1]'))
    ).text
    imdbMovieYearResult = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[2]'))
    ).text
    imdbMovieStarsResult = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[3]'))
    ).text
    imdbMovieResultLink = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a'))).get_attribute("href")
    temp[0] = imdbMovieTitleResult
    driver.close()

    return render(request, 'movies/results.html', {
        'movietitle': imdbMovieTitleResult, 'movieyear': imdbMovieYearResult, 'moviestars': imdbMovieStarsResult,
        'imdburl': imdbMovieResultLink

    })


def search_database(request):
    found = False
    for root, dirs, files in os.walk("/media/HDD1/PlexContent/Movies"):
        for file in files:
            if temp[0] in file:
                found = True
    if found:
        return render(request, "movies/dbsearch.html", {"temp": temp[0] + " Found on Plex Server, no need to download!!"})

    else:
        options = Options()
        options.add_argument("--headless")  # Runs Chrome in headless mode.
        options.add_argument('--no-sandbox')  # # Bypass OS security model
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(chrome_options=options, executable_path=
        r'/home/littlejiver/Downloads/chromedriver_linux64/chromedriver'
                                  )
        # driver = webdriver.Chrome(executable_path=r'/home/littlejiver/Downloads/chromedriver_linux64/chromedriver')
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.zooqle.com/")

        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//div[@id="anp2-wrapper"]//div[text()="NO THANKS"]'))).click()
        wait.until(
            ec.element_to_be_clickable((By.XPATH, '//input[@name="q"]'))
        ).send_keys(temp[0])

        searchBar = wait.until(ec.element_to_be_clickable((By.XPATH, '//div[@class="tt-dataset tt-datas'
                                                           + 'et-qs"]//p[@class="tt-wrap tt-suggestion '
                                                           + 'tt-selectable"]//span[text()="'
                                                           + temp[0] + '"]')))
        searchBar.click()
        wait.until(ec.element_to_be_clickable(
            (By.XPATH,
             '//*[@id="body_container"]/div/div[1]/div[2]/div/table/tbody/tr[2]/td[2]/a'))).click()
        magnetLink = wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="dlPanel"]/div[2]/ul/li[2]/a')))
        torrentLink = magnetLink.get_attribute("href")
        qb = Client("http://www.on-demandlogistics.com:8080/")
        qb.login("admin", "adminadmin")
        qb.download_from_link(torrentLink)
        task = torrent_downloading_progress.delay(1)
        return render(request, "movies/dbsearch.html", {"temp": "Downloading " + temp[0].title() + " now!", 'task_id': task.task_id})


def progress_bar(request):
    task = torrent_downloading_progress.delay(1)
    return render(request, "movies/progressbar.html", {'task_id': task.task_id})
