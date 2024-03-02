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
            api.upload_folder(
                folder_path=file_path,
                repo_id=repo_id,
                repo_type=repo_type,
                path_in_repo=caminho
            )
            return (f"Arquivo {file_name} enviado com sucesso para o repositório {repo_id}.",)
        except Exception as e:
            return (f"Erro ao enviar arquivo para o repositório: {e}",)

# Mapeamento das classes de nós personalizados
NODE_CLASS_MAPPINGS = {
    "UploadToHuggingFaceNode": UploadToHuggingFaceNode
}
