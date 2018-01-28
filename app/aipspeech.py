from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '10462370'
API_KEY = 'xGFG6Bz1WRXf40CGLjh4Ns6PCa6Bgt8M'
SECRET_KEY = '45X0mnZzIVqugr4XOtfspm6ywjAGj26h'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


result  = client.synthesis('你好百度', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
