import pandas as pd
import numpy as np

# Caminho do arquivo CSV
file_path = r"C:\Users\caiod\OneDrive\Documentos\Projetos Python\IC\Imagens Finais\GEM CERN\Imagens"

# Ler o arquivo CSV
df_summary = pd.read_csv(file_path + r"\Summary.csv")
a = df_summary.iloc[:, 4] # Selecionar a coluna 4
c = df_summary.iloc[:, 7] # Selecionar a coluna 7
counts = df_summary.iloc[:, 2]
print(np.sum(counts))

circ = c.to_numpy() # Converter a coluna para um array do NumPy
areas = a.to_numpy() # Converter a coluna para um array do NumPy

df_stddev = pd.read_csv(file_path + r"\summary_stddev.csv")
s_a = df_stddev.iloc[:, 1]
stddevs_areas = s_a.to_numpy()
s_c = df_stddev.iloc[:, 2]
stddevs_circ = s_c.to_numpy()

stddevs_areas = stddevs_areas / np.sqrt(counts)
stddevs_circ = stddevs_circ / np.sqrt(counts)

pesos_a = 1/stddevs_areas**2
pesos_c = 1/stddevs_circ**2

# Calcular a média ponderada
media_ponderada_areas = np.sum(areas * pesos_a) / np.sum(pesos_a)
inc_media_ponderada = np.sqrt(1 / np.sum(pesos_a))
media_ponderada_circ = np.sum(circ * pesos_c) / np.sum(pesos_c)
inc_media_ponderada_circ = np.sqrt(1 / np.sum(pesos_c))

print(f'Média ponderada das areas: {int(np.around(media_ponderada_areas))} ± {int(np.around(inc_media_ponderada))} \u03BCm²')
raio_medio = np.sqrt(media_ponderada_areas / np.pi)
inc_raio_medio = inc_media_ponderada / (2 * np.sqrt(media_ponderada_areas*np.pi))

print(f'Raio médio: {raio_medio:.4f} ± {inc_raio_medio:.4f} \u03BCm')
print(f'Média ponderada das circularidades: {media_ponderada_circ:.5f} ± {inc_media_ponderada_circ:.5f}')