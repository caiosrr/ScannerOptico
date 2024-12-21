import cv2

# Modificar caminhos conforme necessário

pos_x = 0.00
pos_y = 0.00
passo = 2.359 # Indicar passo utilizado
linhas_concatenadas = []  # Lista para armazenar as linhas concatenadas

N = 43  # Número de imagens na grade (Pega a coordenada maxima obtida divide pelo passo e soma 1)
# Loop para concatenar imagens horizontalmente e armazenar as linhas
for i in range(N):
    pos_x = 0.00
    imagem_colada_x = None
    for j in range(N):
        pos_x = j * passo
        imagem = cv2.imread(fr"C:\Users\caiod\OneDrive\Documentos\Projetos Python\IC\Imagens Finais\GEM CERN\Imagens\X_{round(pos_x, 2)}-Y_{round(pos_y, 2)}.png")
        if imagem_colada_x is None:
            imagem_colada_x = imagem
        else:
            imagem_colada_x = cv2.hconcat([imagem_colada_x, imagem])
    linhas_concatenadas.append(imagem_colada_x)
    pos_y += passo

# Inverte a lista para corrigir a ordem de concatenação
linhas_concatenadas = linhas_concatenadas[::-1]

# Concatenação vertical de todas as linhas armazenadas
imagem_final = cv2.vconcat(linhas_concatenadas)

# Salva a imagem final
cv2.imwrite(r"C:\Users\caiod\OneDrive\Documentos\Projetos Python\IC\Imagens Finais\GEM CERN\image_final.png", imagem_final)