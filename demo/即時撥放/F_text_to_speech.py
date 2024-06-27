# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 00:37:17 2023

@author: Handsome
"""
# =============================================================================
# 
# curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) -H "Content-Type: application/json; charset=utf-8" --data "{
#   'input':{
#     'text':'I\'ve added the event to your calendar.'
#   },
#   'voice':{
#     'languageCode':'en-gb',
#     'name':'en-GB-Standard-A',
#     'ssmlGender':'FEMALE'
#   },
#   'audioConfig':{
#     'audioEncoding':'MP3'
#   }
# }" ""
# 
# 
# =============================================================================
def _analyze_res(data):
    import json
    # 將 bytes 轉換為 string
    data_str = data.decode('utf-8')
    
    # 解析 JSON 資料
    json_data = json.loads(data_str)
    
    # 取出 choices 中的回應內容
    response = json_data['audioContent']
    return response

def _download(base64_str,output_file):#將base64加密文字解密後，存檔
    import base64
    import io
    from pydub import AudioSegment
    
    decoded_bytes = base64.b64decode(base64_str)
    
    # 將解碼後的內容轉換為AudioSegment對象
    audio_file = io.BytesIO(decoded_bytes)#將解碼後的內容轉換為可讀取的音訊檔案
    audio_file.seek(0)
    audio_segment = AudioSegment.from_file(audio_file)
    # 將AudioSegment對象寫入wav檔案
    audio_segment.export(output_file, format="wav")

    
def play_audio(file):
    import os
    from pydub import AudioSegment            # 載入 pydub 的 AudioSegment 模組
    from pydub.playback import play           # 載入 pydub.playback 的 play 模組
    
    song = AudioSegment.from_file(file)  # 開啟聲音檔案
    play(song)                                    # 播放聲音
#%%
def TTS(api_key,text,file_path,v_lang,v_name):
    """
    v_lang:為何種語言，v_name為該語言的語氣
    
    語言不對還好，語氣不對 就很可怕了
    """
    import os
    import requests 
    import json
    
    
    
    url='https://texttospeech.googleapis.com/v1/text:synthesize?key='+api_key#transcriptions

    
    payload={
      "audioConfig": {
        "audioEncoding": "LINEAR16",
      },
      "input": {
        "text": text
      },
      "voice": {
        "languageCode": v_lang,
        "name": v_name
      }
    }
    api_key="asdas21d32as13d2as13d21asda"
    headers={
        "Content-Type": "application/json; charset=utf-8",
    }
    files=json.dumps(payload)
    r = requests.post(url, data=files, headers=headers)
    try:
        #解析回傳資料 僅取出r.content中 json格式中的content
        res=_analyze_res(r.content)   
        _download(res,file_path)#將base64加密文字 丟進來
    except:
        print("發生錯誤:")

    return r
            
#r=text_to_speech("請用自己的KEY","今天天氣不錯，但我好累，這幾天有點操，明天終於星期五了 噢耶","test_voice.wav","en-US","cmn-TW-Wavenet-C")
#play_audio("test_voice.wav")

