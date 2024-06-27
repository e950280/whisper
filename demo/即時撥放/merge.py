import F_openai
import F_whisper_api
import F_text_to_speech
import os
import threading
import keyboard
from C_Recorder import Recorder


openai_api_key="sk-請用自己的KEY"
google_api_key="請用自己的KEY"




lang={
      #"cmn-TW":{'gpt_lang':'中文','v_lang':'cmn-TW','v_name':'cmn-TW-Wavenet-C'},
      #"cmn-CN":{'gpt_lang':'中文','v_lang':'cmn-CN','v_name':'cmn-CN-Wavenet-C'},
      "ja-JP":{'gpt_lang':'日文','v_lang':'ja-JP','v_name':'ja-JP-Wavenet-B'},
      "ko-KR":{'gpt_lang':'韓文','v_lang':'ko-KR','v_name':'ko-KR-Wavenet-C'},
      "en-US":{'gpt_lang':'英文','v_lang':'en-US','v_name':'en-US-Wavenet-G'},
      "en-IN":{'gpt_lang':'英文','v_lang':'en-IN','v_name':'en-IN-Wavenet-D'},
      
      "original":{}#僅供建立資料夾時使用，後pop()
      }

sele_lang="ja-JP"

#創建給音檔存放的資料夾
if not os.path.exists('mp3'):
    os.makedirs('mp3')
    
mp3_path="./mp3/"
    
#創建存放的資料夾們
if not os.path.exists('mp3/original'):
    os.makedirs('mp3/original')
if not os.path.exists('mp3/'+sele_lang):
    os.makedirs('mp3/'+sele_lang)

lang.popitem()
mp3_path="./mp3/"



count=0
#count 計算第幾句
recorder=Recorder()

print("開始程式\n")
print("開始錄音:z\n結束錄音:c\n結束程式:Enter")
while True:
    if(keyboard.is_pressed('enter')):
        print("\n結束程式")
        break
    if(keyboard.is_pressed('z')):
        count+=1 #初始為0，從1開始記數
        print("startRecording_{}".format(count))
        recorder.start_recording()
        while True:
            if keyboard.is_pressed('c') :
                recorder.stop_recording()
                recorder.save_to_file(mp3_path+'original/'+"{}_.mp3".format(count))
                print("StopRecording_{}".format(count))
                res=F_whisper_api.whisper(openai_api_key, mp3_path+'original/'+"{}_.mp3".format(count))
                print("\t(原文為:{})".format(res))
                translate=F_openai.gpt(openai_api_key,lang[sele_lang]['gpt_lang'],res)
                print("\t(翻譯為:{})\n".format(translate))
                F_text_to_speech.TTS(google_api_key,translate,mp3_path+sele_lang+"/{}_.mp3".format(count),lang[sele_lang]['v_lang'],lang[sele_lang]['v_name'])
                F_text_to_speech.play_audio(mp3_path+sele_lang+"/{}_.mp3".format(count))
                print("開始錄音:z\n結束錄音:c\n結束程式:Enter")
                break








