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
        command = ["python", "/home/studio-lab-user/test/ComfyUI/custom_nodes/split.py", "--image", image_path, "--output", output_path]

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
    "SplitNode": SplitNode
}
