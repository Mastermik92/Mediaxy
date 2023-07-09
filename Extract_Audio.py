#!/usr/bin/env python3
#Import the required libraries
import os, platform
import subprocess
import logging
import json
from os.path import abspath, dirname

test = 0
olvaszt = 0
                #Terminalban futtatni, durationt nem találja

selo = 0
kivalasztott_sorszam = []
#print('The script was run from', folder_path)
#print('The selected files/folders:\n', selected_files)
#000157801

if test == 0:
    print("Nem teszt")
    folder_path = os.getcwd()
    try:
        selected_files = os.environ["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"]
        selected_files = selected_files.split('\n')[:-1]
    except:
        pass
    selo = selected_files
else:
    print("Teszt")
    #selo = range(1)
    selo = ["11.mkv"]
    folder_path = "11/11"
    selected_files = "11.mkv"


logger = logging.getLogger('mylogger')

handler = logging.FileHandler('mylog.log')
logger.addHandler(handler)
logger.warning(" ")
logger.warning(selected_files)
logger.critical('This is a CRITICAL message')

def okok():
    print('The script was run from')
    logger.warning("kezdodik")
    if test == 1:
        logger.warning("test")
    else:
        logger.warning("selected_files: ")
        logger.warning(selected_files)
    numbering = 0
    for ppp in selo:# selo:
        logger.warning("ppp : ")
        logger.warning(ppp)
        if test == 0:
            logger.warning("not a test")
            #Escape karakter
            #file_path = ppp.replace(" ", "\ ").replace("(", "\(").replace(")", "\)")
            #file_path = file_path.replace("(", "\(")
            #file_path = file_path.replace(")", "\)")
            file_path = ppp
        else:
            file_path = selected_files
            logger.warning("test")
        #Célfájl
        logger.warning("Celfajl")
        #dest_path = file_path.replace(".mkv", " inprogress.mka").replace(".mp4", " inprogress.mka").replace(".avi", " inprogress.mka")
        dest_path = file_path.replace(".mkv", " inprogress.mka")
        dest_path = dest_path.replace(".mp4", " inprogress.mka")
        dest_path = dest_path.replace(".avi", " inprogress.mka")
        logger.warning("Hoooo")
        logger.warning(dest_path)
        mycommand1 = "-i"
        mycommand2 = ["-map", "0:a", "-acodec", "copy"]
        myCommand = ("ffmpeg",mycommand1,file_path,*mycommand2,dest_path)
        logger.warning("myCommand")
        print("myCommand: ",myCommand)
        logger.warning(myCommand)
        #myCommand = "ffmpeg" + " -i " + file_path + " -map 0:a -acodec copy " + dest_path
        logger.warning(kivalasztott_sorszam)
        logger.warning("LOOPOLGATAS")
        lang = []
        jjj = get_metadata(file_audio_languages,kivalasztott_sorszam[numbering]) #get file_audio_languages
        for www in jjj:
            lang.append(www)
 #       for u in kivalasztott_sorszam:
 #           logger.warning(u)
 #           lang = []
  #          for w in file_audio_languages[u]:
 # #              jjj = w.replace("", "")
 #               jjj = w.strip("'")
 #               lang.append(jjj)
 #               logger.warning(lang)
 #           logger.warning(lang)
        logger.warning(lang)
        logger.warning(str(lang))
        finished_filename = dest_path.replace("inprogress", str(lang))
        logger.warning("finished_filename")
        logger.warning(finished_filename)
        #os.system(myCommand)
        subprocess.call(myCommand)
        os.rename(dest_path, finished_filename)
        print("Finished ",dest_path)
        numbering += 1
def get_metadata(typey,number):
    return typey[number]



# Define the arrays to store the information
file_names = []
file_sizes = []

file_video_durations = []
file_video_codec_1 = []
file_video_codec_2 = []
file_video_codec_3 = []
file_video_width = []
file_video_height = []
file_video_def = []
file_video_forced = []

file_audio_channels = []
file_audio_codecs = []
file_audio_languages = []
file_audio_duration = []
file_audio_codec = []
file_audio_def = []
file_audio_forced = []

file_subtitles = []
file_sub_languages = []
file_sub_durations = []
file_sub_def = []
file_sub_forced = []
def get_media_info():
    logger.warning("get_media_info kezdodik")
    print("get_media_info kezdodik")
    print(os.listdir(folder_path))
    logger.warning(os.listdir(folder_path))
# Loop through all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4") or filename.endswith(".mkv") or filename.endswith(".avi"):
            # Store the file name
            file_names.append(filename)
            logger.warning(filename)

            # Use ffprobe to get information about the video file
            result = subprocess.Popen(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_format', os.path.join(folder_path, filename)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = result.communicate()[0]
            video_info = json.loads(output)
            print(video_info)
            # Store the file size
            print("MI a format: ",format)
            file_sizes.append(video_info['format']['size'])
#Video section
            video_codec_1 = []
            video_codec_2 = []
            video_codec_3 = []
            video_width = []
            video_height = []
            video_durations = []
            video_def= []
            video_forced = []

            for stream in video_info['streams']:
                if stream['codec_type'] == 'video':
                    try:
                        video_durations.append(stream['duration'])# mp4
                    except KeyError:
                        try:
                            video_durations.append(stream['tags']['DURATION-eng'])# mkv
                        except KeyError:
                            try:
                                video_durations.append(stream['tags']['DURATION'])# mkv2
                            except KeyError:
 #                           finally:#if there is no duration, get from the audio
                                video_durations.append(video_info["format"]['duration'])
#                               pass
                    video_codec_1.append(stream['codec_name'])
                    video_codec_2.append(stream['codec_long_name'])
                    video_codec_3.append(stream['codec_tag_string'])
                    video_width.append(stream['width'])
                    video_height.append(stream['height'])
                    video_def.append(stream['disposition']['default'])
                    video_forced.append(stream['disposition']['forced'])
#                if video_durations == []:   #Could not find duration metadata in the video section
#                    video_durations.append(video_info["format"]['duration'])
            file_video_codec_1.append(video_codec_1)
            file_video_codec_2.append(video_codec_2)
            file_video_codec_3.append(video_codec_3)
            file_video_width.append(video_width)
            file_video_height.append(video_height)
            file_video_durations.append(video_durations)
            file_video_def.append(video_def)
            file_video_forced.append(video_forced)


#Audio section
            logger.warning(str(filename + " audio kezdodik"))
            print(str(filename + " audio kezdodik"))
            audio_channels = []
            audio_languages = []
            audio_duration = []
            audio_codec = []
            audio_def = []
            audio_forced = []
            for stream in video_info['streams']:
                if stream['codec_type'] == 'audio':
                    audio_channels.append(stream['channels'])
                    try:
                        audio_languages.append(stream['tags']['language'])
                    except KeyError:
                        audio_languages.append('und')
                    audio_codec.append(stream['codec_name'])
                    try:
                        audio_duration.append(stream['duration'])
                    except KeyError:
                        try:
                            audio_duration.append(stream['tags']['DURATION-eng'])
                        except KeyError:
                            try:
                                audio_duration.append(stream['tags']['DURATION'])
                            except KeyError:
                                audio_duration.append('N/A')
                    audio_def.append(stream['disposition']['default'])
                    audio_forced.append(stream['disposition']['forced'])
            file_audio_channels.append(audio_channels)
            file_audio_languages.append(audio_languages)
            file_audio_duration.append(audio_duration)
            file_audio_codec.append(audio_codec)
            file_audio_def.append(audio_def)
            file_audio_forced.append(audio_forced)

#Subtitle section
            logger.warning(str(filename + " Subtitle kezdodik"))
            print(str(filename + " Subtitle kezdodik"))
            sub_channels = []
            sub_languages = []
            sub_duration = []
            sub_def = []
            sub_forced = []

            for stream in video_info['streams']:
                if stream['codec_type'] == 'subtitle':
                    sub_channels.append(stream['codec_name'])
                    try:
                        sub_languages.append(stream['tags']['language'])
                    except KeyError:
                        sub_languages.append('und')
                    try:
                        sub_duration.append(stream['duration'])#??????? Audiobol masolva.,  nem tudom suboknal is elofordulhat e hogy így szerepel
                    except KeyError:
                        try:
                            sub_duration.append(stream['tags']['DURATION-eng'])
                        except KeyError:
                            sub_duration.append('N/A')
                    sub_def.append(stream['disposition']['default'])
                    sub_forced.append(stream['disposition']['forced'])

            file_subtitles.append(sub_channels)
            file_sub_languages.append(sub_languages)
            file_sub_durations.append(sub_duration)
            file_sub_def.append(sub_def)
            file_sub_forced.append(sub_forced)
    # Identify the selected files
    print("Identify the selected files")
    print("selected_files: ",selo)
    logger.warning("Identify the selected files. selected_files: ")
    logger.warning(selo)
    print("file_names: ",file_names)
    for vvv in selo:#Selected files
        for ccc, files in enumerate(file_names):#Loop through all media files found
            print("vvv: ",vvv)
            print("folder_path+/+files: ",folder_path+"/"+files)
            logger.warning(folder_path+"/"+files)
            if folder_path+"/"+files == vvv:
                kivalasztott_sorszam.append(ccc)
                logger.warning("Találat! ccc:")
                print("Találat! ccc: ", ccc)
                logger.warning(ccc)





# Print out the arrays for testing
    print("Nev ",file_names)
    print("Size ",file_sizes)
    print("Dur ",file_video_durations)#.size() video chanelek szama
    print("Codec ",file_video_codec_1)
    print("Codec2 ",file_video_codec_2)
    print("Codec3 ",file_video_codec_3)
    print("X ",file_video_width)
    print("Y ",file_video_height)
    print("Channels ",file_audio_channels)
    print("Lang ",file_audio_languages)
    print("Audio Hossz ",file_audio_duration)
    print("Audio Codec ",file_audio_codec)
    print("Subtitles ",file_subtitles)
    print("Subtitle languages ",file_sub_languages)
    print("Subtitle dur ",file_sub_durations)
    print("Subtitle def ",file_sub_def)
    print("Subtitle f ",file_sub_forced)
    print("kivalasztott_sorszam ",kivalasztott_sorszam)

    logger.warning(file_names)
    logger.warning(file_sizes)
    logger.warning(file_video_durations)
    logger.warning(file_video_codec_1)
    logger.warning(file_video_codec_2)
    logger.warning(file_video_codec_3)
    logger.warning(file_video_width)
    logger.warning(file_video_height)
    logger.warning(file_audio_channels)
    logger.warning(file_audio_languages)
    logger.warning(file_audio_duration)
    logger.warning(file_audio_codec)
    logger.warning(file_subtitles)
    logger.warning(file_sub_languages)
    logger.warning(file_sub_durations)
    logger.warning(file_sub_def)
    logger.warning(file_sub_forced)
    logger.warning(kivalasztott_sorszam)
    logger.warning(kivalasztott_sorszam)
    logger.warning(kivalasztott_sorszam)
    logger.warning(kivalasztott_sorszam)


get_media_info()
okok()
