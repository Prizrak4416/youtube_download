from pytube import YouTube
import ffmpeg
from pathlib import Path
from pydub import AudioSegment


DIR = Path(__file__).resolve().parent
VIDEO_PATH = DIR.joinpath('video')
AUDIO_PATH = DIR.joinpath('audio')

url_youtube = input("enter URL_youtube: ")
print('\n')


def out_red(text):
    return "\033[31m {}\033[0m".format(text)


def out_green(text):
    return "\033[32m {}\033[0m".format(text)


def get_video_audio(url):
    """Get parameters video from youtube url

        Get parameters from youtube, chooses 1080p video and
        audio 128kbps

    :param str url:
        The html contents.
    :return:
        parameters video content and audio content
    """
    video = YouTube(url)
    list_video = video.streams
    video_mas = []
    audio_mas = []

    for i in list_video:
        if i.resolution == "1080p":
            video_mas.append((i.fps, i))
        if i.type == 'audio':
            audio_mas.append((i.abr, i))
    try:
        video_for_download = max(video_mas, key=lambda k: video_mas[0])[1]
        print(out_green('vidio - '), video_for_download)
    except:
        video_for_download = False
    audio_for_download = ''

    for value, key in audio_mas:
        if value == "128kbps":
            audio_for_download = key
        elif audio_for_download == '':
            audio_for_download = key

    print(out_green('audio - '), audio_for_download)

    return [video_for_download, audio_for_download, video.title.replace('\\', ' ').replace('/', ' ').replace('\'', ' ').replace('\"', ' ')]


def download_video(videoParam):
    """ Download FulHD video with youtube

    :param videoParam:
        video parameters on youtube
    :return:
        return the path to the video file
    """
    videoParam.download(filename='video', output_path=DIR)
    input_video = ffmpeg.input(VIDEO_PATH.with_suffix('.mp4'))
    return input_video


def download_audio(audioParam):
    """Download audio with youtube

    :param audioParam:
        audio parameters on youtube
    :return:
        return the path to the audio file
    """
    audioParam.download(filename='audio', output_path=DIR)
    if Path(AUDIO_PATH.with_suffix('.mp4')).exists():
        input_audio = ffmpeg.input(AUDIO_PATH.with_suffix('.mp4'))
    else:
        input_audio = ffmpeg.input(AUDIO_PATH.with_suffix('.webm'))
    return input_audio


def create_video(videoPath, audioPath, titleFile):
    """ combines video and audio file

    :param videoPath:
        path to the video file
    :param audioPath:
        path to the audio file
    :param titleFile:
        name video on youtube
    :return: None
    """
    output_path = DIR.joinpath(titleFile).with_suffix('.mp4')
    try:
        ffmpeg.concat(videoPath, audioPath, v=1, a=1).output(str(output_path)).run()
    except:
        output_path = DIR.joinpath('new_file').with_suffix('.mp4')
        ffmpeg.concat(videoPath, audioPath, v=1, a=1).output(str(output_path)).run()


def create_audio(titleFile):
    """ converting audio file to mp3

    :param titleFile:
        name video on youtube
    :return: None
    """
    if Path(AUDIO_PATH.with_suffix('.mp4')).exists():
        mp4_version = AudioSegment.from_file(AUDIO_PATH.with_suffix('.mp4'), "mp4")
    else:
        mp4_version = AudioSegment.from_file(AUDIO_PATH.with_suffix('.webm'), "webm")
    mp4_version.export(DIR.joinpath(titleFile).with_suffix('.mp3'), format="mp3")


def del_file():
    """ delet audio file and video file downloaded with youtube

    :return: None
    """
    path = Path(VIDEO_PATH.with_suffix('.mp4'))
    if Path(path).exists():
        path.unlink()
    if Path(AUDIO_PATH.with_suffix('.mp4')).exists():
        path = Path(AUDIO_PATH.with_suffix('.mp4'))
        path.unlink()
    elif Path(AUDIO_PATH.with_suffix('.webm')).exists():
        path = Path(AUDIO_PATH.with_suffix('.webm'))
        path.unlink()


print('1 - Download video with audio FulHD')
print('2 - Download audio mp3')
number = input(out_green('Push number - '))

if int(number) == 1:
    video, audio, title = get_video_audio(url_youtube)
    if video == False:
        print(out_red("video with 1080p don't have"))
    else:
        videoPath = download_video(video)
        audioPath = download_audio(audio)
        create_video(videoPath, audioPath, title)
elif int(number) == 2:
    video, audio, title = get_video_audio(url_youtube)
    audioPath = download_audio(audio)
    create_audio(title)
else:
    print(out_red('incorrect values entered'))

del_file()
