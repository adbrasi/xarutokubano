import os
from datetime import datetime
from huggingface_hub import HfApi, login

class UploadToHuggingFaceNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {}),
                "repo_id": ("STRING", {}),
                "token": ("STRING", {})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "upload_to_huggingface"
    CATEGORY = "custom"

    def upload_to_huggingface(self, file_path, repo_id, token):
        # Login no Hugging Face Hub
        login(token=token)

        # Identificação do tipo de repositório
        repo_type = "model"

        # Obter o nome do arquivo
        file_name = os.path.basename(file_path)

        # Obter a data atual e formatá-la
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d-%m")

        # Caminho no repositório Hugging Face Hub
        caminho = f"/{data_formatada}/{file_name}"

        try:
            # Realizar o upload do arquivo para o repositório no Hugging Face Hub
            api = HfApi()
            api.upload_file(
                path_or_fileobj=file_path,
                repo_id=repo_id,
                repo_type=repo_type,
                path_in_repo=caminho
            )
            return (f"Arquivo {file_name} enviado com sucesso para o repositório {repo_id}.",)
        except Exception as e:
            return (f"Erro ao enviar arquivo para o repositório: {e}",)


import subprocess

class SplitMaskNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_path": ("STRING", {}),
                "mask_path": ("STRING", {})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute_split_mask"
    CATEGORY = "custom"

    def execute_split_mask(self, image_path, mask_path):
        # Comando a ser executado
        command = ["python", "/home/studio-lab-user/ComfyUI/custom_nodes/xarutokubano/mask-separation.py", "--image", image_path, "--mask", mask_path]
        try:
            # Executar o comando usando subprocess
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            # Capturar a saída do processo
            output = result.stdout.strip()
            return (output,)
        except subprocess.CalledProcessError as e:
            # Se ocorrer um erro, retornar uma mensagem de erro
            return (f"Erro ao executar o comando: {e.stderr}",)

        
import subprocess

class SplitNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_path": ("STRING", {}),
                "output_path": ("STRING", {})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute_split"
    CATEGORY = "custom"

    def execute_split(self, image_path, output_path):
        # Comando a ser executado
        command = ["python", "/home/studio-lab-user/ComfyUI/custom_nodes/split.py", "--image", image_path, "--output", output_path]

        try:
            # Executar o comando usando subprocess
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            # Capturar a saída do processo
            output = result.stdout.strip()
            return (output,)
        except subprocess.CalledProcessError as e:
            # Se ocorrer um erro, retornar uma mensagem de erro
            return (f"Erro ao executar o comandox: {e.stderr}",)

import os
import zipfile

class ZipFolderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "zip_folder"
    CATEGORY = "custom"

    def zip_folder(self, folder_path):
        # Verifica se o caminho é de uma pasta válida
        if not os.path.isdir(folder_path):
            return (f"O caminho '{folder_path}' não é uma pasta válida.",)

        # Obtém o nome da pasta
        folder_name = os.path.basename(folder_path)

        # Define o nome do arquivo zip
        zip_file_path = os.path.join('/home/studio-lab-user/ComfyUI/custom_nodes/xarutokubano/zipes', f"{folder_name}.zip")

        try:
            # Cria o arquivo zip
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Percorre todos os arquivos e subpastas dentro da pasta
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Adiciona o arquivo ao arquivo zip preservando a estrutura de pastas
                        zipf.write(file_path, os.path.relpath(file_path, folder_path))

            return (zip_file_path,)
        except Exception as e:
            return (f"Ocorreu um erro ao comprimir a pasta '{folder_path}': {e}",)



import subprocess

class LorabyNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute_loraby"
    CATEGORY = "custom"

    def execute_loraby(self, input_string):
        # Comando a ser executado
        command = [
            "python", 
            "/content/wildcards/loraby.py",
            "-input",
            input_string,
            "-json",
            "/content/file.json"
        ]

        try:
            # Executar o comando usando subprocess
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            # Capturar a saída do processo
            output = result.stdout.strip()
            return (output,)
        except subprocess.CalledProcessError as e:
            # Se ocorrer um erro, retornar uma mensagem de erro
            return (f"Erro ao executar o comando: {e.stderr}",)

    


        
# Mapeamento das classes de nós personalizados
NODE_CLASS_MAPPINGS = {
    "ZipFolderNode": ZipFolderNode,
    "UploadToHuggingFaceNode": UploadToHuggingFaceNode,
    "SplitNode": SplitNode,
    "find Lora by token": LorabyNode,
    "SplitMaskNode": SplitMaskNode
}
