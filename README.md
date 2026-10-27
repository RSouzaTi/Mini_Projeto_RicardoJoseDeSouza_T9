# Análise exploratória de dados de varejo

**Aluno:** Ricardo José de Souza  
**Turma:** T9

O projeto prepara dados de compras de varejo e produz um relatório de qualidade,
estatísticas descritivas e agrupamentos com Python, pandas e Rich.

Fonte: [Base Varejo no Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data).

## Instalação e execução

No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python importacao_dados.py
python Limpeza_dados.py
python Resumo.py
```

A importação exibe registros, colunas, tipos, nulos por coluna, duplicatas e
uma amostra. A limpeza salva a tabela tratada; o resumo lê exclusivamente
essa saída. Execute novamente as duas últimas etapas após modificar a entrada.
Os caminhos são relativos à pasta dos scripts, não ao diretório do terminal.

## Organização

| Arquivo | Finalidade |
| --- | --- |
| `Base_Varejo.csv` | Entrada preservada |
| `Base_varejo_original.csv` | Saída limpa, sobrescrita pela limpeza; o nome foi mantido por compatibilidade |
| `importacao_dados.py` | Leitura estruturada com csv.DictReader e leitura tabular com pandas |
| `Limpeza_dados.py` | Padronização, validação, separação de registros inválidos e deduplicação |
| `Resumo.py` | Indicadores, estatísticas, agrupamentos e conclusões |
| `formatacao.py` | Exibição com Rich e formatação de números |
| `requirements.txt` | Dependências pandas e Rich |
| `resultados/` | Relatórios, estatísticas, agrupamentos e registros rejeitados gerados na execução |

## Colunas

| Coluna | Conteúdo |
| --- | --- |
| DATA | Data da compra |
| CO_ID | Identificador da compra |
| CL_ID | Identificador do cliente |
| CL_GENERO | Gênero informado |
| CL_EC | Código do estado civil |
| CL_FHL | Número de filhos |
| CL_SEG | Segmento |
| PR_ID | Identificador do produto ou SKU |
| PR_CAT | Categoria |
| PR_NOME | Nome do produto |

O estado civil é apresentado pelo código, sem atribuir rótulos sem um
dicionário de dados confirmado. Uma linha representa uma ocorrência de produto;
uma compra pode conter várias linhas.

## Regras de limpeza e qualidade

- Remover colunas totalmente vazias e normalizar espaços em textos com expressão regular.
- Preencher categorias vazias com `Sem Categoria` usando if/else.
  Nome, gênero e segmento ausentes recebem `Não informado`.
- Converter códigos e filhos para inteiros anuláveis. IDs devem ser positivos
  e inteiros; filhos e estado civil não podem ser negativos ou fracionários.
  O domínio dos códigos de estado civil ainda depende de dicionário confirmado.
- Converter datas no padrão dia/mês/ano usando datetime; datas impossíveis
  são consideradas inválidas.
- Separar linhas sem IDs essenciais ou datas válidas em
  `resultados/registros_rejeitados.csv`.
- Adotar a hipótese operacional de que um CO_ID corresponde a um cliente e
  uma data; compras conflitantes também são separadas. A atividade não define
  uma regra mais específica para o identificador.
- Eliminar linhas idênticas após padronização, mantendo um registro.
- Preservar filhos ausentes como nulos: zero significaria afirmar que o
  cliente não tem filhos. As estatísticas ignoram esses valores e mostram a
  contagem válida.
- Registrar quantos dados entraram, foram separados, deduplicados e mantidos.
  Uma verificação de reconciliação confere esses totais.

Não há preço, quantidade nem dimensões físicas nesta base. Portanto, não há
imputação de dimensões nem conversão de valores monetários para float.
As médias e demais medidas estatísticas são números decimais.

## Estatísticas e agrupamentos

São calculadas todas as medidas solicitadas para CL_FHL:

**Contagem, média, mediana, desvio padrão amostral, todas as modas, mínimo,
máximo, primeiro quartil, segundo quartil e terceiro quartil.**

Os resultados são apresentados por registro e por cliente único.
Para clientes, usa-se o perfil na data mais recente. Quando há perfis
conflitantes nessa mesma data, o cliente é excluído somente dos indicadores
demográficos, e a quantidade de exclusões é informada.

O relatório inclui agrupamentos por gênero, segmento, código de estado civil,
categoria e mês. Categoria e mês apresentam contagens de registros e de compras
distintas. As compras por categoria não são aditivas, pois uma compra pode
conter várias categorias. Empates nas categorias e produtos líderes são preservados.

## Resultados verificados

Na execução com a cópia local da base de 830.000 registros:

1. Foram removidas 96.553 duplicatas, restando **733.447 registros**; não houve
   rejeições por IDs, datas ou conflitos de compra nessa execução.
2. A base limpa contém **18.471 compras e 1.000 clientes**.
3. O perfil mais recente dos clientes apresenta **519 códigos F e 481 códigos M**,
   sem perfis ambíguos na última data.
4. **ALIMENTOS** lidera com **384.197 registros**; o produto mais frequente é
   **PAPINHA INFANTIL, SKU 51**, com **3.322 registros**.
5. Por cliente, a média de filhos é **1,136**, a mediana e a moda são **0**,
   e o desvio padrão amostral é **1,413330**.
6. A deduplicação pode remover repetições legítimas de produtos; sem quantidade
   nem identificador do item, essa hipótese precisa ser validada com a origem.

| Medida de filhos | Por cliente | Por registro |
| --- | ---: | ---: |
| Contagem válida | 1.000 | 733.447 |
| Média | 1,136000 | 1,146049 |
| Mediana | 0 | 0 |
| Desvio padrão amostral | 1,413330 | 1,416917 |
| Moda | 0 | 0 |
| Mínimo | 0 | 0 |
| Quartil 25% | 0 | 0 |
| Quartil 50% | 0 | 0 |
| Quartil 75% | 2 | 2 |
| Máximo | 4 | 4 |

Esses valores dependem da versão da entrada. O programa gera conclusões
atualizadas a cada execução.

## Saídas

Além da base limpa, são gerados:

- `resultados/limpeza.txt`: diagnóstico final e contadores de limpeza.
- `resultados/estatisticas_filhos.csv`: estatísticas por cliente e registro.
- `resultados/agrupamento_*.csv`: agrupamentos.
- `resultados/relatorio.txt`: indicadores, estatísticas e conclusões.
- `resultados/conclusoes.md`: seis tópicos gerados com os dados.
- `resultados/registros_rejeitados.csv`: linhas separadas e motivo.

## Reflexão sobre ETL

ETL significa Extração, Transformação e Carga. Aqui, a extração verifica a
estrutura do CSV com DictReader e o carrega com pandas; a transformação
padroniza textos, converte tipos e valida registros; a carga grava a base
limpa e os relatórios para análise.

Tratar ausências exige compreender o significado de cada campo. Substituir
filhos ausentes por zero alteraria a interpretação; identificadores ausentes
impedem relacionar uma linha com segurança. Por isso, o tratamento é específico
por coluna, e registros inválidos são separados para revisão.

A remoção de duplicatas é uma hipótese documentada, não uma prova de que as
linhas repetidas eram erros. Preservar a entrada, explicar as regras e
reconciliar as contagens permite revisar essa decisão. Os indicadores medem
ocorrências e compras distintas; não permitem inferir faturamento ou unidades
físicas sem os campos correspondentes.

## Validação

A limpeza e o resumo foram executados sobre a cópia local completa da base.
Também foram conferidos exemplos com datas impossíveis, IDs negativos e
fracionários, compra com clientes conflitantes, categoria vazia, filhos
ausentes e duplicatas. As medidas estatísticas foram comparadas com uma
sequência de valores conhecidos, incluindo quartis e desvio padrão amostral.
