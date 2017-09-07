# https://stackoverflow.com/questions/37725416/pydub-combine-split-on-silence-with-minimum-length-file-size
import numpy as np
import os

from pydub import AudioSegment
# from pydub.silence import split_on_silence


def split_MFCC_by_audio_times(audioTimesPath=None, audioMFCCPath=None, mfccStepInMs=10):
    # Read audio times file
    audioTimes = read_audio_times(audioTimesPath=audioTimesPath)
    # Read audio MFCC file
    audioMFCC = read_audio_MFCC_file(audioMFCCPath=audioMFCCPath)
    # Check
    if audioMFCC is None or audioTimes is None:
        return None
    # Output
    audioMFCCChunks = []
    # For each audio chunk
    for audioChunkTime in audioTimes:
        # Extract audio chunk
        audioMFCCChunks.append(audioMFCC[int(audioChunkTime[0]/mfccStepInMs):int(audioChunkTime[1]/mfccStepInMs)])
    # Return
    return audioMFCCChunks


def read_audio_times(audioTimesPath=None):
    # If no audio times file is provided
    if audioTimesPath == None or not os.path.isfile(audioTimesPath):
        print("Please provide a valid audio times file path!", audioTimesPath, "not valid!")
        return None
    # Read times file
    audioTimes = []
    with open(audioTimesPath) as f:
        for line in f:
            startTimes = line[:-1].split(' ')[1].split(':')
            startTimeInMs = int(int(startTimes[0])*1000*60*60 + int(startTimes[1])*1000*60 + float(startTimes[2])*1000)
            endTimes = line[:-1].split(' ')[2].split(':')
            endTimeInMs = int(int(endTimes[0])*1000*60*60 + int(endTimes[1])*1000*60 + float(endTimes[2])*1000)
            audioTimes.append([startTimeInMs, endTimeInMs])
    # Result
    return audioTimes


def read_audio_file(audioPath=None):
    # If no audio file is provided
    if audioPath == None or not os.path.isfile(audioPath):
        print("Please provide a valid audio file path!", audioPath, "not valid!")
        return None
    fileFormat = audioPath.split('.')[-1]
    return AudioSegment.from_file(audioPath, format=fileFormat)


def read_audio_MFCC_file(audioMFCCPath=None):
    # If no audio file is provided
    if audioMFCCPath == None or not os.path.isfile(audioMFCCPath):
        print("Please provide a valid audio MFCC file path!", audioMFCCPath, "not valid!")
        return None
    # Extract file format
    fileFormat = audioMFCCPath.split('.')[-1]
    # npy: the result of applying pyAudioAnalysis to the mp3 file: eg. "/home/voletiv/Datasets/BG/1/BG-C15.mp3_st.npy"
    # eg. python audioAnalysis.py featureExtractionFile -i /home/voletiv/Datasets/BG/1/BG-C15.mp3 -mw 1.0 -ms 1.0 -sw 0.020 -ss 0.010 -o /home/voletiv/Datasets/BG/1/BG-C15.mp3
    if fileFormat == 'npy':
        return np.load(audioMFCCPath).T
    # csv
    elif fileFormat == 'csv':
        print("MFCC file format is csv. Support not yet built, please input an npy file.")
    # else
    else:
        print("MFCC file format", fileFormat,"not supported!")


# EXTRACT MFCC FEATURES USING pyAudioAnalysis
python audioAnalysis.py featureExtractionFile -i /home/voletiv/Datasets/BG/1/BG-C15.mp3 -mw 1.0 -ms 1.0 -sw 0.020 -ss 0.010 -o /home/voletiv/Datasets/BG/1/BG-C15.mp3

mfccFeatures = np.load('/home/voletiv/Datasets/BG/1/BG-C15.mp3_st.npy')


# def split_audio_at_silences(audioPath=None, min_silence_len=1000, silence_thresh=-16, keep_silence=200):
#     # Read audio file
#     sound = read_audio_file(audioPath=audioPath)
#     if sound == None:
#         return None
#     # Split on silence
#     chunks = split_on_silence(
#         sound,
#         # split on silences longer than 1000ms (1 sec)
#         min_silence_len=min_silence_len,
#         # anything under -16 dBFS is considered silence
#         silence_thresh=silence_thresh, 
#         # keep 200 ms of leading/trailing silence
#         keep_silence=keep_silence
#     )
#     # now recombine the chunks so that the parts are at least 90 sec long
#     target_length = 90 * 1000
#     output_chunks = [chunks[0]]
#     for chunk in chunks[1:]:
#         if len(output_chunks[-1]) < target_length:
#             output_chunks[-1] += chunk
#         else:
#             # if the last output chunk is longer than the target length,
#             # we can start a new one
#             output_chunks.append(chunk)
#     # Output
#     return output_chunks


# # REMOVING NOISE

# audioPath = '/home/voletiv/Datasets/BG/1/BG-C15.mp3'
# noise = sound[7000:12000]

# min_silence_len = 900
# silence_thresh = -16
# keep_silence = 80

# chunks = split_audio_at_silences(audioPath=audioPath, fileFormat="mp3", min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=keep_silence)
