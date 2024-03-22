import json
import os
import argparse

def obter_lora_file(json_file, token):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    for item in data:
        if item['token'] == token:
            return item['lora_file']
    
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Obter lora_file correspondente a um token em um arquivo JSON.')
    parser.add_argument('-input', dest='node_input_wild', required=True, help='Token de entrada')
    parser.add_argument('-json', dest='json_file', required=True, help='Caminho para o arquivo JSON')
    args = parser.parse_args()

    lora_file = obter_lora_file(os.path.expanduser(args.json_file), args.node_input_wild)

    if lora_file:
        print(lora_file)
    else:
        print("Token não encontrado no arquivo JSON.")
