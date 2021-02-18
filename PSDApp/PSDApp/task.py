from celery import shared_task
from qbittorrent import Client
from time import sleep
@shared_task(bind=True)
def torrent_downloading_progress(self, duration):
    sleep(duration)

    # qb = Client("http://www.on-demandlogistics.com:8080/")
    # qb.login("admin", "adminadmin")
    # downloading_progress_live = 0
    # for x in range(100):
    #     progress = int(
    #         qb.get_torrent(
    #             "cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_downloaded"]
    #         / qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_size"] * 100
    #                         )
    #     downloading_progress_live = progress
    return 'Done!'
