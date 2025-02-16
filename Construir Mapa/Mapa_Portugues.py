import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math

# Caminho do arquivo CSV
file_path = r"C:\Users\caiod\OneDrive\Documentos\Projetos Python\IC\Imagens Finais\GEM CERN\Imagens"

# Ler o arquivo CSV
df = pd.read_csv(file_path + r"\Summary.csv")

# Obter os nomes das imagens, áreas e circularidades
image_names = df.iloc[:, 1]  # Selecionar a coluna 1 (com nomes como X_2.33-Y_2.33)
a = df.iloc[:, 4]  # Selecionar a coluna 4 (áreas)
areas = a.to_numpy()  # Converter a coluna de áreas para NumPy array
raios = np.sqrt(areas / np.pi)  # Calcular os raios

# Obter a circularidade da coluna 7
circ = df.iloc[:, 7]  # Selecionar a coluna 7 (circularidade)
circularidades = circ.to_numpy()  # Converter a coluna de circularidade para NumPy array

# Função para extrair coordenadas do nome da imagem (Exemplo: X_2.33-Y_2.33)
def extract_coordinates(image_name):
    match = re.match(r"X_(\d+(\.\d+)?)\-Y_(\d+(\.\d+)?)", image_name)
    if match:
        x = float(match.group(1))
        y = float(match.group(3))
        return x, y
    return None, None

# Dicionário para armazenar os raios e circularidades com suas coordenadas (X, Y)
coord_raios = {}
coord_circularidades = {}

# Iterar sobre os nomes das imagens e preencher os dicionários
for i, name in enumerate(image_names):
    x, y = extract_coordinates(name)
    if x is not None and y is not None:
        coord_raios[(x, y)] = raios[i]
        coord_circularidades[(x, y)] = circularidades[i]
    else:
        print(f"Falha ao extrair coordenadas de {name}")

# Definir dimensões do grid
dim = 100
passo = 2.359
dim_passo = math.ceil(dim / passo)

# Criar matrizes para armazenar os valores dos raios e circularidades (mapas de calor)
heatmap_raios = np.full((dim_passo, dim_passo), np.nan)  # Inicializar com NaN
heatmap_circularidades = np.full((dim_passo, dim_passo), np.nan)  # Inicializar com NaN

# Preencher os heatmaps com base nas coordenadas extraídas
for (x, y), raio in coord_raios.items():
    i = int(np.round(x / passo))  # Usar np.round para garantir melhor arredondamento
    j = int(np.round(y / passo))
    
    # Verificar se os índices estão dentro do intervalo
    if 0 <= i < dim_passo and 0 <= j < dim_passo:
        heatmap_raios[j, i] = raio
    else:
        print(f"Coordenadas fora do intervalo: X={x}, Y={y}")

# Preencher o heatmap de circularidades
for (x, y), circularidade in coord_circularidades.items():
    i = int(np.round(x / passo))  # Usar np.round para garantir melhor arredondamento
    j = int(np.round(y / passo))
    
    # Verificar se os índices estão dentro do intervalo
    if 0 <= i < dim_passo and 0 <= j < dim_passo:
        heatmap_circularidades[j, i] = circularidade
    else:
        print(f"Coordenadas fora do intervalo: X={x}, Y={y}")

# Função para mostrar os mapas de calor
def mostrar_mapas_de_calor():
    plt.figure(figsize=(10, 5))

    # Mapa de calor dos raios
    plt.subplot(1, 2, 1)
    plt.imshow(heatmap_raios, extent=[0, dim, 0, dim], origin='lower', cmap='viridis')
    plt.colorbar(label='Raio [µm]')
    plt.xlabel('X [mm]')
    plt.ylabel('Y [mm]')
    plt.title('Mapa de raios do GEM')

    # Mapa de calor das circularidades
    plt.subplot(1, 2, 2)
    plt.imshow(heatmap_circularidades, extent=[0, dim, 0, dim], origin='lower', cmap='plasma')
    plt.colorbar(label='Circularidade')
    plt.xlabel('X [mm]')
    plt.ylabel('Y [mm]')
    plt.title('Mapa de circularidades do GEM')

    plt.tight_layout()
    plt.show()

# Função para mostrar o histograma dos raios
def mostrar_histograma_raios():
    plt.figure()
    plt.hist(raios, bins=20, color='blue', edgecolor='black')
    plt.xlabel('Raio [µm]', fontsize=20)  # Aumenta a fonte do rótulo do eixo X
    plt.ylabel('Frequência', fontsize=20)  # Aumenta a fonte do rótulo do eixo Y
    plt.title('Histograma dos Raios', fontsize=25)  # Aumenta a fonte do título
    plt.xticks(fontsize=12)  # Aumenta a fonte dos ticks do eixo X
    plt.yticks(fontsize=12)  # Aumenta a fonte dos ticks do eixo Y
    plt.show()

# Função para mostrar o histograma das circularidades
def mostrar_histograma_circularidades():
    plt.figure()
    plt.hist(circularidades, bins=13, color='yellow', edgecolor='black')
    plt.xlabel('Circularidade', fontsize=20)  # Aumenta a fonte do rótulo do eixo X
    plt.ylabel('Frequência', fontsize=20)  # Aumenta a fonte do rótulo do eixo Y
    plt.title('Histograma das Circularidades', fontsize=25)  # Aumenta a fonte do título
    plt.xticks(fontsize=12)  # Aumenta a fonte dos ticks do eixo X
    plt.yticks(fontsize=12)  # Aumenta a fonte dos ticks do eixo Y
    plt.show()


# Mostrar os gráficos em sequência
mostrar_mapas_de_calor()
mostrar_histograma_raios()
mostrar_histograma_circularidades()