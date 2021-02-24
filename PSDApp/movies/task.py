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
        for x in qb.torrents(category='PSDApp'):
            print(progress_recorder)
            progress_recorder.set_progress(round(float(x["progress"]*100), 1), 100)
            if x['state'] != "uploading":
                downloading = False
            else:
                continue
