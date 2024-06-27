def analyze_whisper_res(data):
    import json
    # 將 bytes 轉換為 string
    data_str = data.decode('utf-8')
    
    # 解析 JSON 資料
    json_data = json.loads(data_str)
    
    response = json_data['text']

    return response

#%%
def whisper(api_key,file_path):
    import os
    import openai
    import requests 
    import json
    
    openai.api_key = api_key
    
    
    url='https://api.openai.com/v1/audio/transcriptions'#transcriptions
    
    
    with open(file_path, 'rb') as file:
    
        payload={
            "file": file,
            "model":  (None, 'whisper-1'),
        }
    
        headers={
            "Authorization": f"Bearer {openai.api_key}",
        }
        
        r = requests.post(url, files=payload, headers=headers)
    
        try:
            #解析回傳資料 僅取出r.content中 json格式中的content
            #res=analyze_res()   
            res=analyze_whisper_res(r.content)   
            return res
            
        except:
            print("發生錯誤:",r.content)

#whisper('sk-請用自己的API', './audio2.mp3')