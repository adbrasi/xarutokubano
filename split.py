import cv2
import numpy as np
import os
import random
import string
from PIL import Image
import argparse
import shutil

# Função para recortar e salvar os pedaços da imagem com fundo transparente
def excluir_arquivos_pequenos(pasta_output):
    try:
        # Verifica se a pasta de saída existe
        if os.path.exists(pasta_output) and os.path.isdir(pasta_output):
            # Itera sobre os arquivos na pasta
            for arquivo in os.listdir(pasta_output):
                # Obtém o caminho completo do arquivo
                caminho_arquivo = os.path.join(pasta_output, arquivo)
                # Verifica se é um arquivo regular e seu tamanho é menor que 999 bytes
                if os.path.isfile(caminho_arquivo) and os.path.getsize(caminho_arquivo) < 9 * 1024:
                    # Remove o arquivo
                    os.remove(caminho_arquivo)
                    
        else:
            print("A pasta de saída não existe.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        
def recortar_e_salvar(imagem, contornos, output_path, tamanho_minimo_contorno=30):
    # Gera um nome aleatório para a pasta dentro do output_path
    nome_pasta = ''.join(random.choices(string.ascii_lowercase, k=5))
    pasta_output = os.path.join(output_path, nome_pasta)
    os.makedirs(pasta_output)

    # Função para encontrar as dimensões do conteúdo não transparente
    def encontrar_dimensoes_nao_transparentes(imagem):
        largura, altura = imagem.size
        esquerda, topo, direita, inferior = largura, altura, 0, 0

        # Percorrer a imagem em busca de pixels não transparentes
        for x in range(largura):
            for y in range(altura):
                if imagem.getpixel((x, y))[3] != 0:  # Verificar o canal alfa (transparência)
                    # Atualizar as coordenadas do conteúdo não transparente
                    esquerda = min(esquerda, x)
                    topo = min(topo, y)
                    direita = max(direita, x)
                    inferior = max(inferior, y)

        # Calcular as dimensões do conteúdo não transparente
        largura_nao_transparente = direita - esquerda + 1
        altura_nao_transparente = inferior - topo + 1

        return (esquerda, topo, largura_nao_transparente, altura_nao_transparente)

    # Função para recortar e centralizar o conteúdo não transparente
    def recortar_centralizar_conteudo(imagem):
        # Encontrar as dimensões do conteúdo não transparente
        esquerda, topo, largura, altura = encontrar_dimensoes_nao_transparentes(imagem)

        # Recortar o conteúdo não transparente
        recorte = imagem.crop((esquerda, topo, esquerda + largura, topo + altura))

        # Criar uma nova imagem do tamanho do recorte
        nova_imagem = Image.new("RGBA", (largura, altura), (255, 255, 255, 0))

        # Colar o recorte no centro da nova imagem
        nova_imagem.paste(recorte, (0, 0))

        return nova_imagem

    # Loop sobre os contornos
    for i, contorno in enumerate(contornos):
        # Calcula a área do contorno
        area_contorno = cv2.contourArea(contorno)

        # Verifica se o contorno atende ao tamanho mínimo
        if area_contorno < tamanho_minimo_contorno:
            continue

        # Gera o nome aleatório para a imagem
        nome_imagem = nome_pasta + '-' + str(i+1) + '.png'

        # Cria uma imagem preta com o mesmo tamanho da imagem original
        img = np.zeros_like(imagem)

        # Desenha o contorno na imagem preta
        cv2.drawContours(img, [contorno], -1, (255, 255, 255), thickness=cv2.FILLED)

        # Converte a imagem preta para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Threshold para criar uma máscara
        mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

        # Junta a imagem original com a máscara para criar um fundo transparente
        result = np.dstack((imagem, mask))

        # Cria uma imagem PIL a partir da matriz numpy
        result_pil = Image.fromarray(result)

        # Recorta e centraliza o conteúdo não transparente
        nova_imagem = recortar_centralizar_conteudo(result_pil)

        # Salva a imagem recortada e centralizada
        nova_imagem.save(os.path.join(pasta_output, nome_imagem))

    return pasta_output

def main():
    parser = argparse.ArgumentParser(description='Split alpha pieces from an image')
    parser.add_argument('--output', dest='output_path', required=True, help='Output path')
    parser.add_argument('--image', dest='image_path', required=True, help='Input image path')
    args = parser.parse_args()

    # Carrega a imagem em BGR
    imagem = cv2.imread(args.image_path)

    # Converte a imagem para escala de cinza
    imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Encontra os contornos usando o método findContours
    contornos, _ = cv2.findContours(imagem_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Converte a imagem de BGR para RGB
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

    # Chama a função para recortar e salvar os pedaços da imagem com fundo transparente
    pasta_output = recortar_e_salvar(imagem_rgb, contornos, args.output_path, tamanho_minimo_contorno=40)

    # Remove arquivos pequenos da pasta de saída
    excluir_arquivos_pequenos(pasta_output)

    # Copia a imagem de entrada para a pasta de saída
    shutil.copy(args.image_path, pasta_output)

    print(pasta_output)

if __name__ == "__main__":
    main()
