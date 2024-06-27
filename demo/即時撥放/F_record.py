# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 22:52:23 2023

@author: Handsome
"""


    
def save(stream,frames,wav_name,mp3_name): 
    from pydub import AudioSegment            # 載入 pydub 的 AudioSegment 模組
    import wave

    print("結束")
    stream.stop_stream() 
    stream.close()
    wf = wave.open(wav_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()  
    wav_to_mp3(wav_name,mp3_name)

def wav_to_mp3(wav_name,mp3_name):
    from pydub import AudioSegment
    #song = AudioSegment.from_mp3("song.mp3")        # 讀取背景音樂 mp3 檔案
    voice = AudioSegment.from_wav(wav_name) # 讀取錄音 wav 檔案
    #output = voice.overlay(song, loop=True)         # 混合錄音和背景音樂
    #play(output)                                    # 播放聲音
    voice.export(mp3_name)                     # 輸出為 mp3

def record_one(wav_path,mp3_path,wav_name,mp3_name):
    import keyboard
    import pyaudio
    import os
    global chunk, sample_format, channels, fs, seconds, file_count,audio #不想省那一點空間 讓程式碼變醜
    
    # 設定錄音參數
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2  
    fs = 44100
    seconds = 15
    file_count=0
    audio = pyaudio.PyAudio()
    
    
    
    

    # 開始錄音
    print("開始錄音:z\n結束錄音:c\n")   
    
    while True:
        if(keyboard.is_pressed('z')):
            #重新開始錄音 做初始化
            print("開始錄音")
            frames = []
            stream=audio.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)
            
            while True:
                data = stream.read(chunk)
                frames.append(data) 
                if keyboard.is_pressed('c'):
                    break
            temp_wav_name=wav_path+wav_name
            temp_mp3_name=mp3_path+mp3_name
            save(stream,frames,temp_wav_name,temp_mp3_name)
            break
    #結束程式前 關閉錄音、播放等音訊相關的任務。
    audio.terminate()
def record(wav_path,mp3_path,wav_name,mp3_name):
    import keyboard
    import pyaudio
    import os
    global chunk, sample_format, channels, fs, seconds, file_count,audio #不想省那一點空間 讓程式碼變醜
    
    # 設定錄音參數
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2  
    fs = 44100
    seconds = 15
    file_count=0
    audio = pyaudio.PyAudio()
    
    
    
    
    
    
    # 開始錄音
    print("開始錄音(暫定最高15秒 可無上限):z\n結束錄音:c\n結束程式:enter\n")   
    
    while True:
        if(keyboard.is_pressed('enter')):
            print("結束程式")
            break
        if(keyboard.is_pressed('z')):
            #重新開始錄音 做初始化
            print("開始錄音")
            file_count+=1
            frames = []
            stream=audio.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)
            
            while True:
                data = stream.read(chunk)
                frames.append(data) 
                if keyboard.is_pressed('c') or len(frames) >= int(44100 / chunk * seconds):
                    break
            temp_wav_name=str(file_count)+'_'+wav_name
            temp_mp3_name=str(file_count)+'_'+mp3_name
            save(stream,frames,temp_wav_name,temp_mp3_name)
            
    #結束程式前 關閉錄音、播放等音訊相關的任務。
    audio.terminate()

#record("AAA.wav","BBB.mp3")
#record_one("./wav/","./mp3/","test.wav",'ttt.mp3')