import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

class CohereIaService:
    def obter_info_alimento(self, produto):
        api_key = os.getenv('API_KEY_COHERE') 

        prompt = f'''
        {{
            "nome": "",
            "descricao": "",
            "nutrientes": {{
                "calorias": "",
                "carboidratos": "",
                "proteinas": "",
                "gorduras": "",
                "fibra_alimentar": "",
                "vitaminas": {{
                    "vitamina_C": "",
                    "vitamina_B9": ""
                }},
                "minerais": {{
                    "ferro": "",
                    "magnésio": "",
                    "potassio": ""
                }}
            }}
        }}

        Alimente os valores desse arquivo JSON com informações do alimento que será informado. Mantenha o valor da chave 'descricao' resumido. 
        Observações: 
        -Instrução Importante: Se o parâmetro fornecido não corresponder a um alimento, retorne apenas a string: 'O parâmetro informado não é um alimento.' em vez de um objeto JSON.
        -Não retorne nada diferente ou além do que foi informado nessas instruções. 
        O produto é: {produto}
        '''

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': 'command-r-08-2024',
            'preamble': "You are Command, a brilliant, sophisticated, AI-assistant chatbot trained to assist human users by providing thorough responses.",
            'temperature': 0.3,
            'message': prompt
        }

        print(json.dumps(data, indent=2)) 

        endpoint_cohere = os.getenv('ENDPOINT_COHERE') 

        response = requests.post(endpoint_cohere, headers=headers, json=data, stream=True)

        if response.status_code == 200:
            resposta_final = ""
            for line in response.iter_lines():
                if line:  
                    try:
                        linha_json = json.loads(line) 
                        if linha_json.get("result", {}).get("eventType") == "STREAM_EVENT_TYPE_TEXT_GENERATION":
                            texto = linha_json["result"]["textGenerationStreamEvent"]["text"]
                            resposta_final += texto  
                    except json.JSONDecodeError as e:
                        print("Erro ao decodificar a linha JSON:", line)
                        print("Erro:", e) 
            return resposta_final
        else:
            print(f"Erro na requisição à API: {response.text}") 
            return json.dumps({"message": "Erro na requisição à API", "status_code": response.status_code, "error": response.text}, ensure_ascii=False)
        