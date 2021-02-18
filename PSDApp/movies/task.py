from celery import shared_task
from celery_progress.backend import ProgressRecorder
from qbittorrent import Client
from time import sleep


@shared_task(bind=True)
def torrent_downloading_progress(self, duration):
    progress_recorder = ProgressRecorder(self)
    sleep(duration)
    qb = Client("http://www.on-demandlogistics.com:8080/")
    qb.login("admin", "adminadmin")
    downloading = True
    while downloading:
        for x in qb.torrents():
            progress_recorder.set_progress(float(x["progress"])*100, 100)
            if float(x["progress"]) == 100.00:
                downloading = False


    # for i in range(100):
    #     sleep(1)
    #     progress_recorder.set_progress(i + 1, 100)
    #
    # for i in range(100):
    # if float(qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_downloaded"]) > float(qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_size"]):
    #     progress = int(
    #         qb.get_torrent(
    #             "cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_downloaded"]
    #         / qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_size"] * 100
    #                         )
    #     print(qb.get_torrent(
    #             "cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_downloaded"]
    #         / qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_size"] * 100
    #                         )
    # # int(qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_downloaded"] / int(
    # #         qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_size"]))
    #     progress_recorder.set_progress(
    #         int(qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_downloaded"])), int(
    #         qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_size"])

# downloading_progress_live = 0
    # for x in range(100):
    #     progress = int(
    #         qb.get_torrent(
    #             "cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_downloaded"]
    #         / qb.get_torrent("cca0bf46ce95c802e6a8f0e1f353978d12da6997")["total_size"] * 100
    #                         )
    #     downloading_progress_live = progress




    return 'Done!'
