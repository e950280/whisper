import F_openai
import F_whisper_api
import F_text_to_speech
import os
import threading
import keyboard
from C_Recorder import Recorder
#import time 

def worker(count):
    print("{}開始".format(count))
    res=F_whisper_api.whisper(openai_api_key, mp3_path+'original/'+"{}_.mp3".format(count))
    with open(text_path+"original/{}_.txt".format(count), 'w', encoding='utf-8') as f:
        f.write(res)
    
    
    #sele_lang 為當前迴圈 為何種語言
    #轉各國語言時 再平行處理
    for sele_lang in lang:
        t=threading.Thread(target=worker_GPT_TTS,args=(count,res,sele_lang,))
        t.start()
    print("{}結束".format(count))    
    
def worker_GPT_TTS(count,res,sele_lang):
    #print("翻譯----"+sele_lang+"\t\t"+time.strftime( "%Y-%m-%d %I :%M:%S %p" , time.localtime()) )
    translate=F_openai.gpt(openai_api_key,lang[sele_lang]['gpt_lang'],res)
    with open(text_path+sele_lang+"/{}_.txt".format(count), 'w', encoding='utf-8') as f:
        f.write(translate)
    #print("轉語音----"+sele_lang+"\t\t"+time.strftime( "%Y-%m-%d %I :%M:%S %p" , time.localtime()) )
    F_text_to_speech.TTS(google_api_key,translate,mp3_path+sele_lang+"/{}_.mp3".format(count),lang[sele_lang]['v_lang'],lang[sele_lang]['v_name'])
    #print("轉換語言{}完成\t".format(sele_lang)+time.strftime( "%Y-%m-%d %I :%M:%S %p" , time.localtime()) )
    
    
openai_api_key="sk-請用自己的API"
google_api_key="請用自己的API"

lang={
      #"cmn-TW":{'gpt_lang':'中文','v_lang':'cmn-TW','v_name':'cmn-TW-Wavenet-C'},
      #"cmn-CN":{'gpt_lang':'中文','v_lang':'cmn-CN','v_name':'cmn-CN-Wavenet-C'},
      "ja-JP":{'gpt_lang':'日文','v_lang':'ja-JP','v_name':'ja-JP-Wavenet-B'},
      "ko-KR":{'gpt_lang':'韓文','v_lang':'ko-KR','v_name':'ko-KR-Wavenet-C'},
      "en-US":{'gpt_lang':'英文','v_lang':'en-US','v_name':'en-US-Wavenet-G'},
      "en-IN":{'gpt_lang':'英文','v_lang':'en-IN','v_name':'en-IN-Wavenet-D'},
      
      "original":{}#僅供建立資料夾時使用，後pop()
      }

#sele_lang="cmn-TW" #之後或許可以作為 設定此程式為了哪種語言服務，可提升精確度 還可以節省成本與錯誤率(比如原文為中文，還丟去gpt 讓他翻成中文)



#創建存放的資料夾們
for sele_lang in lang:
    if not os.path.exists('mp3/'+sele_lang):
        os.makedirs('mp3/'+sele_lang)
    if not os.path.exists('text/'+sele_lang):
        os.makedirs('text/'+sele_lang)
lang.popitem()
mp3_path="./mp3/"
text_path='./text/'


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
                t=threading.Thread(target=worker,args=(count,))
                t.start()
                print("開始錄音:z\n結束錄音:c\n結束程式:Enter")

                break

        
        
    
