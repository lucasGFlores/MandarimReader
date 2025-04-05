import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract

from src.searchers.cccedict.dictionary import CeDictionary
from src.HMI.pyside.interface import Interface

def preprocess_image(image_path):
    # Passo 1: Carregar e converter para escala de cinza
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # Passo 2: Redução de ruído
    # denoised = cv2.bilateralFilter(gray, 2,100,100)

    # Passo 3: Binarização
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bitwised = cv2.bitwise_not(binary)

    # Passo 4: Ajuste de contraste/nitidez
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(12, 12))
    contrasted = clahe.apply(bitwised)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(contrasted, -1, kernel)
    # Aplica a operação de fechamento (remove buracos)
    sharpened = cv2.morphologyEx(sharpened, cv2.MORPH_OPEN, np.array((5,5),np.uint8))
    # Passo 5: Redimensionamento
    resized = cv2.resize(sharpened, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Salvar imagem processada
    cv2.imwrite("processed_image.jpg", resized)
    return resized





def ocr_tesseract(preprocessed_image):
    pil_image = Image.fromarray(preprocessed_image)
    text = pytesseract.image_to_string(
        pil_image,
        lang="chi_tra_vert",
        config="--psm 5"  # Modo de segmentação para orientação vertical
    )
    parsed_text = ''.join(text.split(" "))
    print("Texto tesseract: ",parsed_text)
    return  parsed_text  #do parse


# def ocr_by_recreation():
#     hanzi = "我是巴西人"  # Caractere para gerar
#     hanzi = list(hanzi)
#     hanzi = "\n".join(hanzi)
#     font_path = "notosans.ttf"  # Arquivo de fonte chinês (ex: SimHei)
#     image_size = (250, 600)  # Tamanho da imagem
#     background_color = (255, 255, 255)  # Cor de fundo (branco)
#     text_color = (0, 0, 0)  # Cor do texto (preto)
#     font_size = 150
#
#     # Criar imagem com Pillow
#     img_pil = Image.new("RGB", image_size, background_color)
#     draw = ImageDraw.Draw(img_pil)
#
#     # Carregar fonte chinesa
#     try:
#         font = ImageFont.truetype(font_path, font_size)
#     except IOError:
#         print("Erro: Arquivo de fonte não encontrado!")
#         exit()
#
#     # Calcular posição para centralizar o texto
#     text_bbox = draw.textbbox((0, 0), hanzi, font=font)
#     text_width = text_bbox[2] - text_bbox[0]
#     text_height = text_bbox[3] - text_bbox[1]
#     x = (image_size[0] - text_width) / 2
#     y = (image_size[1] - text_height) / 2
#
#     # Desenhar texto na imagem
#     draw.text((x, y), hanzi, font=font, fill=text_color)
#
#     # Converter para array numpy (OpenCV)
#     img_np = np.array(img_pil)
#
#     # Converter RGB para BGR (OpenCV usa BGR)
#     img_opencv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
#
#     # Salvar imagem
#     cv2.imwrite("hanzi.png", img_opencv)
#
#     # Mostrar imagem
#     cv2.imshow("Hanzi", img_opencv)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def main():
    # image = preprocess_image("./imagens/juju1.png")
    # if image is None:
    #     print("Erro ao carregar a imagem.")
    #     return
    #
    # text = ocr_tesseract(image)
    # dict_ = CeDictionary()
    # print(dict_.search_data(text))
    inter = Interface()
    inter.start()

def test_binary_tree():
    print("creating the binary tree")






if __name__ == "__main__":
    main()