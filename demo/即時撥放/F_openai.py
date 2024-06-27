def _analyze_res(data):
    import json
    # 將 bytes 轉換為 string
    data_str = data.decode('utf-8')
    
    # 解析 JSON 資料
    json_data = json.loads(data_str)
    
    # 取出 choices 中的回應內容
    response = json_data['choices'][0]['message']['content']
    return response

#%%
def gpt(api_key,lang,message):
    """
    """
    import os
    import openai
    import requests 
    import json
    
    openai.api_key = api_key
    
    url='https://api.openai.com/v1/chat/completions'
    
    # 設置對話開始的提示語
    prompt = "請幫我翻譯成合理的"+lang+"內容是:"
    prompt+=message+'\n'
    payload={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
        #"n": 10,
        #"temperature: 0.7
    }

    headers={
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type":"application/json"
    }
    
    
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    try:
        #解析回傳資料 僅取出r.content中 json格式中的content
        res=_analyze_res(r.content)   
        
        prompt +=  res+'\n'
        
        return res
    except:
        print("發生錯誤:",r.content)


