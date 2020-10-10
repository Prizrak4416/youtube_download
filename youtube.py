from pytube import YouTube
import ffmpeg
from pathlib import Path

DIR = '1/'
VIDEO_PATH = '{}video'.format(DIR)
AUDIO_PATH = '{}audio'.format(DIR)

if DIR[-1] != '/':
    DIR += '/'

# url = input("vvedite URL_youteme: ")
url_youtube = 'https://www.youtube.com/watch?v=DPJv5u1EcaM'


def getVideoAudio(url):
    video = YouTube(url)
    list_video = video.streams
    video_mas = []
    audio_mas = []

    for i in list_video:
        if i.resolution == "1080p":
            video_mas.append((i.fps, i))
        if i.type == 'audio':
            audio_mas.append((i.abr, i))

    video_for_download = max(video_mas, key=lambda k: video_mas[0])[1]
    audio_for_download = ''


    for value, key in audio_mas:
        if value == "128kbps":
            audio_for_download = key
        elif audio_for_download == '':
            audio_for_download = key

    return [video_for_download, audio_for_download, video.title]


def downloadVideoAudio(videoParam, audioParam):
    videoParam.download(filename='video', output_path=DIR)
    audioParam.download(filename='audio', output_path=DIR)

    input_video = ffmpeg.input(VIDEO_PATH + '.mp4')
    if Path('1/audio.mp4').exists():
        input_audio = ffmpeg.input(AUDIO_PATH + '.mp4')
    else:
        input_audio = ffmpeg.input(AUDIO_PATH + '.webm')

    return (input_video, input_audio)


def createVideo(videoPath, audioPath, titleFile):
    ffmpeg.concat(videoPath, audioPath, v=1, a=1).output('{}{}.mp4'.format(DIR, titleFile)).run()


def delFile():
    path = Path(VIDEO_PATH + '.mp4')
    path.unlink()
    if Path(AUDIO_PATH + '.mp4').exists():
        path = Path(AUDIO_PATH + '.mp4')
    else:
        path = Path(AUDIO_PATH + '.webm')
    path.unlink()


getVideoAudio(url_youtube)

video, audio, title = getVideoAudio(url_youtube)

videoPath, audioPath = downloadVideoAudio(video, audio)

createVideo(videoPath, audioPath, title)

delFile()



