"""

Mini projeto de análise exploratória de varejo - Ricardo José de Souza.

"""

import csv
import pandas as pd

# Carregando os dados do arquivo CSV
data = pd.read_csv('Base_Varejo.csv', sep=';')
# Exibe as primeiras linhas do DataFrame para inspeção inicial
print(data.head())  

