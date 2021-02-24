from django.shortcuts import render

from qbittorrent import Client
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from movies.task import torrent_downloading_progress

import os
import shutil


movie_name = [""]
movie_year = []



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
    movie_name[0] = imdbMovieTitleResult
    imdbMovieYearResult = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[2]'))
    ).text
    imdbMovieStarsResult = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a/div[2]/div[3]'))
    ).text
    imdbMovieResultLink = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/a'))).get_attribute("href")
    driver.close()

    return render(request, 'movies/results.html', {
        'movietitle': imdbMovieTitleResult, 'movieyear': imdbMovieYearResult, 'moviestars': imdbMovieStarsResult,
        'imdburl': imdbMovieResultLink
    })


def search_database(request):
    found = False
    # update plex media server folder here for movies
    for root, dirs, files in os.walk("/mnt/HDD1/PlexContent/Movies"):
        for file in files:
            if movie_name[0] in file:
                found = True
    if found:
        return render(request, "movies/found.html", {"temp": movie_name[0] + " Found on Plex Server, no need to download!!"})

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
        ).send_keys(movie_name[0])

        searchBar = wait.until(ec.element_to_be_clickable((By.XPATH, '//div[@class="tt-dataset tt-datas'
                                                           + 'et-qs"]//p[@class="tt-wrap tt-suggestion '
                                                           + 'tt-selectable"]//span[text()="'
                                                           + movie_name[0] + '"]')))
        searchBar.click()
        wait.until(ec.element_to_be_clickable(
            (By.XPATH,
             '//*[@id="body_container"]/div/div[1]/div[2]/div/table/tbody/tr[2]/td[2]/a'))).click()
        magnetLink = wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="dlPanel"]/div[2]/ul/li[2]/a')))
        torrentLink = magnetLink.get_attribute("href")
        qb = Client("http://www.on-demandlogistics.com:8080/")
        qb.login("admin", "adminadmin")
        qb.download_from_link(torrentLink, category='PSDApp')
        task = torrent_downloading_progress.delay(1)

        return render(request, "movies/dbsearch.html", {
                    "temp": "Downloading " + movie_name[0].title() + " now!", 'task_id': task.task_id
                                                                })

        # running = True
        # while running:
        #     if task.state == "PENDING":
        #         return render(request, "movies/dbsearch.html", {
        #             "temp": "Downloading " + movie_name[0].title() + " now!", 'task_id': task.task_id
        #                                                         })
        #     elif task.state == "SUCCESS":
        #         return render(request, "movies/moving.html", {})
        #     else:
        #         running = False


def move_video_to_plex_server(request):
    rename_list = []
    list_renamed = []
    torrents = []
    dir_path_needed = ""
    qb = Client("http://www.on-demandlogistics.com:8080/")
    qb.login("admin", "adminadmin")
    for root, dirs, files in os.walk("/home/littlejiver/Downloads/CompletedTorrents"):
        for file in files:
            if not os.path.exists(root.replace("/home/littlejiver/Downloads/CompletedTorrents",
                                               "/mnt/HDD1/PlexContent/Movies")):
                os.mkdir(root.replace("/home/littlejiver/Downloads/CompletedTorrents", "/mnt/HDD1/PlexContent/Movies"))
                shutil.chown(root.replace("/home/littlejiver/Downloads/CompletedTorrents",
                                          "/mnt/HDD1/PlexContent/Movies"), "littlejiver", "plexserver")
            shutil.move(root + "/" + file, root.replace("/home/littlejiver/Downloads/CompletedTorrents",
                                                        "/mnt/HDD1/PlexContent/Movies") + "/" + file)
    for i in qb.torrents(category='PSDApp'):
        torrents.append(i["hash"])
    qb.delete(torrents)
    #         rename_list.append(root + file)
    #
    # i = "/home/littlejiver/Downloads/CompletedTorrents/Rumble In The Bronx (1995) [1080p] [BluRay] [5.1] [YTS.MX]"
    # z = "/mnt/HDD1/PlexContent/Movies/"
    # shutil.move(i, z)
    # print("Moved file!")

    # for i in rename_list:
    #     temp2 = temp.replace(temp, "'" + temp + "'")
    #     print(temp2)
    #     list_renamed.append(temp.replace("/home/littlejiver/Downloads/CompletedTorrents/" + temp2 + "/", "/mnt/HDD1/PlexContent/Movies/" + temp2 + "/"))
    #
    #     for z in list_renamed:
    #         print("file moved from: " + i + " to: " + z)
    #         shutil.move(i, z)
    return render(request, "movies/moving.html", {})
