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
        zip_file_path = os.path.join(os.path.dirname(folder_path), f"{folder_name}.zip")

        try:
            # Cria o arquivo zip
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Percorre todos os arquivos e subpastas dentro da pasta
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Adiciona o arquivo ao arquivo zip preservando a estrutura de pastas
                        zipf.write(file_path, os.path.relpath(file_path, folder_path))

            return (f"'{zip_file_path}'.",)
        except Exception as e:
            return (f"Ocorreu um erro ao comprimir a pasta '{folder_path}': {e}",)

# Mapeamento das classes de nós personalizados
NODE_CLASS_MAPPINGS = {
    "ZipFolderNode": ZipFolderNode
}
