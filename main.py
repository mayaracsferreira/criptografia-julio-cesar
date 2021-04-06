import codecs
import hashlib
import json
import requests

def save_json_file(data):
    with open('answer.json', 'w', encoding='utf-8') as f:
         json.dump(data, f, ensure_ascii=False)

def crypto_resume(data):
    resumo = hashlib.sha1(data['decifrado'].lower().encode('utf-8')).hexdigest()
    data['resumo_criptografico'] = resumo
    return data

def decrypt_message(data):
    alfa = "abcdefghijklmnopqrstuvwxyz"
    number = data['numero_casas']
    encrypted = data['cifrado']
        
    for symbol in encrypted:
        if symbol in alfa:
            position = alfa.index(symbol)
            data['decifrado'] += alfa[position - number]            
        else:
            data['decifrado'] += symbol    
     
    return data

def post_answers():    
    answer = {'answer': open('answer.json','rb')}
    response = requests.post(URI_POST, files=answer)
    print(response.content)

def get_token_from_json():
    f = open('data.json')
    data = json.load(f)    
    f.close()
    return data["token"]


TOKEN = get_token_from_json()
URI_GET = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}".format(TOKEN)
URI_POST = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}".format(TOKEN)

response = requests.get(URI_GET)
data = response.json()
decrypt_message(data)
crypto_resume(data)
save_json_file(data)
post_answers()