"""Tratamento de textos, números, datas, ausências e duplicatas."""
import re
from datetime import datetime
import pandas as pd
from importacao_dados import importar_dados, diagnosticar, CAMINHO_CSV_ORIGINAL, RESULTADOS

def limpar_texto(valor):
    if pd.isna(valor):
        return pd.NA
    texto = re.sub(r"\s+", " ", str(valor)).strip()
    return texto if texto else pd.NA

def converter_data(valor):
    try:
        return datetime.strptime(str(valor), "%d/%m/%Y")
    except (ValueError, TypeError):
        return pd.NaT

def categoria_ou_padrao(valor):
    if pd.isna(valor):
        return "Sem Categoria"
    else:
        return valor

class LimpezaDeDados:
    def __init__(self, df):
        self.df = df.copy()
        self.registros_iniciais = len(df)
        self.rejeitados = df.iloc[:0].copy()
        self.duplicatas = 0
        self.log = {}

    def executar(self):
        diagnosticar(self.df)
        self.df = self.df.dropna(axis=1, how="all")
        obrigatorias = {"DATA", "CO_ID", "CL_ID", "CL_FHL", "CL_GENERO",
                        "CL_EC", "CL_SEG", "PR_ID", "PR_CAT", "PR_NOME"}
        faltam = obrigatorias - set(self.df.columns)
        if faltam:
            raise ValueError(f"Colunas obrigatórias ausentes: {sorted(faltam)}")
        for c in ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]:
            self.df[c] = self.df[c].map(limpar_texto)
        self.log["categorias_preenchidas"] = int(self.df.PR_CAT.isna().sum())
        self.df["PR_CAT"] = self.df["PR_CAT"].map(categoria_ou_padrao)
        for c in ["CL_GENERO", "CL_SEG", "PR_NOME"]:
            self.df[c] = self.df[c].fillna("Não informado")
        for c in ["CL_GENERO", "CL_SEG"]:
            self.df[c] = self.df[c].str.upper()
        for c in ["CO_ID", "CL_ID", "PR_ID", "CL_FHL", "CL_EC"]:
            numeros = pd.to_numeric(self.df[c], errors="coerce")
            validos = numeros.ge(0) & numeros.mod(1).eq(0)
            if c in ["CO_ID", "CL_ID", "PR_ID"]:
                validos &= numeros.gt(0)
            self.log[f"invalidos_{c}"] = int((~validos).sum())
            self.df[c] = numeros.where(validos).astype("Int64")
        mapa = {v: converter_data(v) for v in self.df.DATA.dropna().unique()}
        self.df["DATA"] = pd.to_datetime(self.df.DATA.map(mapa))
        self.log["datas_invalidas_ou_ausentes"] = int(self.df.DATA.isna().sum())
        # Hipótese operacional: um CO_ID pertence a um cliente e uma data.
        # Não se remove uma compra apenas porque contém produtos diferentes.
        grupos = self.df.groupby("CO_ID")[["CL_ID", "DATA"]].nunique()
        conflitos = grupos.index[grupos.gt(1).any(axis=1)]
        invalidos = self.df[["CO_ID", "CL_ID", "PR_ID", "DATA"]].isna().any(axis=1)
        invalidos |= self.df.CO_ID.isin(conflitos)
        self.rejeitados = self.df.loc[invalidos].copy()
        self.rejeitados["MOTIVO"] = "ID/data inválido ou compra com cliente/data conflitante"
        self.df = self.df.loc[~invalidos].copy()
        antes = len(self.df)
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        self.duplicatas = antes - len(self.df)
        assert self.registros_iniciais == len(self.df) + len(self.rejeitados) + self.duplicatas
        return self

    def salvar_novo_csv(self, caminho=CAMINHO_CSV_ORIGINAL):
        RESULTADOS.mkdir(exist_ok=True)
        self.df.to_csv(caminho, sep=";", index=False, date_format="%d/%m/%Y")
        self.rejeitados.to_csv(RESULTADOS / "registros_rejeitados.csv", sep=";", index=False)
        return self

    def mostrar_relatorio(self):
        texto = (
            f"Registros iniciais: {self.registros_iniciais}\n"
            f"Registros rejeitados: {len(self.rejeitados)}\n"
            f"Duplicatas removidas: {self.duplicatas}\n"
            f"Registros finais: {len(self.df)}\n"
            f"Validações: {self.log}\n"
            f"Nulos remanescentes:\n{self.df.isna().sum().to_string()}\n"
            f"Tipos finais:\n{self.df.dtypes.to_string()}\n"
        )
        print(texto)
        RESULTADOS.mkdir(exist_ok=True)
        (RESULTADOS / "limpeza.txt").write_text(texto, encoding="utf-8")
        return self

if __name__ == "__main__":
    LimpezaDeDados(importar_dados()).executar().salvar_novo_csv().mostrar_relatorio()
