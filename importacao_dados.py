"""Leitura da base original e da saída de limpeza."""
import csv
from pathlib import Path
import pandas as pd

PASTA = Path(__file__).resolve().parent
CAMINHO_CSV = PASTA / "Base_Varejo.csv"
# Nome mantido por compatibilidade; este arquivo contém a base LIMPA.
CAMINHO_CSV_ORIGINAL = PASTA / "Base_varejo_original.csv"
RESULTADOS = PASTA / "resultados"

def importar_dados(limpos=False):
    caminho = CAMINHO_CSV_ORIGINAL if limpos else CAMINHO_CSV
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo ausente: {caminho}. Execute a limpeza antes do resumo.")
    # DictReader verifica a estrutura sem guardar todos os registros em memória.
    with caminho.open(encoding="utf-8-sig", newline="") as entrada:
        leitor = csv.DictReader(entrada, delimiter=";")
        for linha in leitor:
            if None in linha or any(v is None for v in linha.values()):
                raise ValueError(f"Linha CSV irregular próxima à linha {leitor.line_num}")
    dados = pd.read_csv(caminho, sep=";", encoding="utf-8-sig", low_memory=False)
    return dados.replace(r"^\s*$", pd.NA, regex=True)

def diagnosticar(df):
    print(f"Registros: {len(df):,}; colunas: {len(df.columns)}")
    print("Colunas e tipos:\n", df.dtypes.to_string())
    print("Nulos por coluna:\n", df.isna().sum().to_string())
    print("Duplicatas completas:", int(df.duplicated().sum()))

if __name__ == "__main__":
    dados = importar_dados()
    diagnosticar(dados)
    print(dados.head())
