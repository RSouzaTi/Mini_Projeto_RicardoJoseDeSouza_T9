"""Indicadores e estatísticas calculados exclusivamente sobre a base limpa."""
import pandas as pd
from rich.panel import Panel
from rich.text import Text
from importacao_dados import importar_dados, RESULTADOS
from formatacao import console, numero_br

def estatisticas_filhos(serie):
    """Desvio padrão amostral, quartis lineares e todas as modas."""
    s = pd.to_numeric(serie, errors="coerce").dropna()
    return pd.Series({
        "Contagem": len(s), "Média": s.mean(), "Mediana": s.median(),
        "Desvio padrão amostral": s.std(ddof=1),
        "Moda(s)": ", ".join(str(int(v)) for v in s.mode()),
        "Mínimo": s.min(), "1º quartil (25%)": s.quantile(.25),
        "2º quartil (50%)": s.quantile(.5), "3º quartil (75%)": s.quantile(.75),
        "Máximo": s.max(),
    })

def mostrar_resumo(df):
    if df.empty:
        raise ValueError("A base limpa está vazia; não há dados para resumir.")
    df = df.copy()
    df["DATA"] = pd.to_datetime(df.DATA, format="%d/%m/%Y", errors="coerce")
    if df.DATA.isna().any():
        raise ValueError("Há datas inválidas na saída. Execute novamente a limpeza.")
    # Se houver perfis distintos na última data de um cliente, não se escolhe
    # arbitrariamente um deles para estatísticas demográficas.
    ultimos = df.loc[df.DATA.eq(df.groupby("CL_ID").DATA.transform("max"))]
    perfil = ["CL_GENERO", "CL_EC", "CL_FHL", "CL_SEG"]
    conflitos = ultimos.groupby("CL_ID")[perfil].nunique(dropna=False).gt(1).any(axis=1)
    ids_conflitantes = conflitos.index[conflitos]
    clientes = ultimos.loc[~ultimos.CL_ID.isin(ids_conflitantes)].drop_duplicates("CL_ID")
    por_genero = clientes.groupby("CL_GENERO", dropna=False).size().rename("clientes")
    por_categoria = df.groupby("PR_CAT", dropna=False).agg(
        registros=("PR_ID", "size"), compras=("CO_ID", "nunique")
    ).sort_values("registros", ascending=False)
    por_mes = df.groupby(df.DATA.dt.to_period("M")).agg(
        registros=("PR_ID", "size"), compras=("CO_ID", "nunique")
    )
    por_segmento = clientes.groupby("CL_SEG", dropna=False).size().rename("clientes")
    por_estado = clientes.groupby("CL_EC", dropna=False).size().rename("clientes")
    produtos = df.groupby(["PR_ID", "PR_NOME"]).size().sort_values(ascending=False)
    datas = df.groupby("DATA").size()
    dias = ", ".join(d.strftime("%d/%m/%Y") for d in datas.index[datas.eq(datas.max())])
    stats_clientes = estatisticas_filhos(clientes.CL_FHL)
    stats_registros = estatisticas_filhos(df.CL_FHL)
    texto = (
        f"Registros: {numero_br(len(df))}\nCompras distintas: {numero_br(df.CO_ID.nunique())}\n"
        f"Clientes distintos: {numero_br(df.CL_ID.nunique())}\n"
        f"Datas com mais registros de itens: {dias}\n"
        f"Clientes com perfil ambíguo na última data: {len(ids_conflitantes)}\n"
        f"Média de filhos por cliente: {numero_br(stats_clientes['Média'], casas=2)}\n"
        f"Clientes por gênero:\n{por_genero.to_string()}\n"
        f"Clientes por segmento:\n{por_segmento.to_string()}\n"
        f"Clientes por código de estado civil:\n{por_estado.to_string()}\n"
    )
    conclusoes = [
        f"A base limpa contém {len(df):,} registros, {df.CO_ID.nunique():,} compras e {df.CL_ID.nunique():,} clientes.",
        f"Clientes por gênero, usando o perfil mais recente sem conflito: {por_genero.to_dict()}.",
        f"Categoria com maior frequência: {', '.join(por_categoria.index[por_categoria.registros.eq(por_categoria.registros.max())].astype(str))}; {int(por_categoria.registros.max()):,} registros por categoria líder.",
        f"Produto(s) com maior frequência: {', '.join(f'SKU {sku} - {nome}' for sku, nome in produtos.index[produtos.eq(produtos.max())])}; {int(produtos.max()):,} registros por produto líder.",
        f"Média de filhos por cliente: {stats_clientes['Média']:.2f}; mediana: {stats_clientes['Mediana']:.2f}; perfis ambíguos excluídos: {len(ids_conflitantes)}.",
        "Limitações: linhas idênticas foram tratadas como duplicatas, mas podem ser repetições legítimas. Sem preço e quantidade, não se calcula faturamento nem unidades físicas. Nulos de filhos são ignorados nas estatísticas, sem substituição por zero.",
    ]
    relatorio = texto + "\nEstatísticas de filhos por cliente único:\n" + stats_clientes.to_string()
    relatorio += "\n\nEstatísticas de filhos por registro:\n" + stats_registros.to_string()
    relatorio += "\n\nAgrupamento por categoria:\n" + por_categoria.to_string()
    relatorio += "\n\nAgrupamento por mês:\n" + por_mes.to_string()
    relatorio += "\n\nConclusões:\n" + "\n".join("- " + c for c in conclusoes)
    console.print(Panel(Text(relatorio), title="Resumo da base limpa", expand=False))
    RESULTADOS.mkdir(exist_ok=True)
    for nome, tabela in [("genero", por_genero), ("segmento", por_segmento),
                        ("estado_civil", por_estado), ("categoria", por_categoria), ("mes", por_mes)]:
        tabela.to_csv(RESULTADOS / f"agrupamento_{nome}.csv", sep=";")
    pd.DataFrame({"por_cliente": stats_clientes, "por_registro": stats_registros}).to_csv(
        RESULTADOS / "estatisticas_filhos.csv", sep=";")
    (RESULTADOS / "relatorio.txt").write_text(relatorio + "\n", encoding="utf-8")
    (RESULTADOS / "conclusoes.md").write_text("\n".join("- " + c for c in conclusoes) + "\n", encoding="utf-8")
    return stats_clientes

if __name__ == "__main__":
    mostrar_resumo(importar_dados(limpos=True))
