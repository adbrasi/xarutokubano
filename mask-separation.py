import os
import cv2
import numpy as np
import argparse



def separar_imagem_por_mascara_avancado(imagem_path, mascara_path, output_dir):
    # Carregar a imagem e a máscara
    imagem = cv2.imread(imagem_path)
    mascara = cv2.imread(mascara_path, cv2.IMREAD_GRAYSCALE)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma máscara acumulativa para evitar sobreposições
    mascara_acumulativa = np.zeros_like(mascara)

    # Criar o diretório de saída se ele não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterar sobre os contornos encontrados
    for i, contour in enumerate(contours):
        # Calcular o retângulo delimitador para o contorno atual
        x, y, w, h = cv2.boundingRect(contour)
        
        # Verificar sobreposição com a máscara acumulativa
        regiao_sobreposta = cv2.bitwise_and(mascara_acumulativa[y:y+h, x:x+w], mascara[y:y+h, x:x+w])

        # Se houver sobreposição, ajustar a máscara atual
        mascara[y:y+h, x:x+w] -= regiao_sobreposta

        # Recortar a região da imagem com base no retângulo delimitador
        imagem_recortada = imagem[y:y+h, x:x+w]

        # Criar uma imagem com canal alfa (transparência)
        imagem_alpha = np.zeros((h, w, 4), dtype=np.uint8)
        imagem_alpha[:, :, :3] = imagem_recortada
        imagem_alpha[:, :, 3] = mascara[y:y+h, x:x+w]

        # Salvar a imagem recortada no diretório de saída
        cv2.imwrite(os.path.join(output_dir, f'imagem_segmentada_{i}.png'), imagem_alpha)

        # Atualizar a máscara acumulativa
        mascara_acumulativa[y:y+h, x:x+w] = np.maximum(mascara_acumulativa[y:y+h, x:x+w], mascara[y:y+h, x:x+w])

    return output_dir

if __name__ == "__main__":
    # Configurar o parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Separar imagem por máscara')
    parser.add_argument('--image', type=str, help='Caminho para a imagem')
    parser.add_argument('--mask', type=str, help='Caminho para a máscara')
    args = parser.parse_args()
    file_name_without_extension = os.path.splitext(os.path.basename(args.image))[0]
    output= f"/home/studio-lab-user/ComfyUI/custom_nodes/xarutokubano/{file_name_without_extension}"
    # Chamar a função para separar a imagem com base na máscara e salvar as imagens segmentadas
    output_dir = separar_imagem_por_mascara_avancado(args.image, args.mask, output)

    print(output_dir)
